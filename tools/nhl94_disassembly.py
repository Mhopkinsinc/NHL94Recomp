#!/usr/bin/env python3
"""
nhl94_disassembly.py - turn the NHL 94 asm68k disassembly into the
recompiler's disassembly-evidence inputs (PRINCIPLES #16: disasm is ground
truth for what is code and where routines begin).

The engine's tests/tools/gen_disasm_*.py scripts parse Macroassembler AS
listings (`NNNN/ HEXOFFS :` rows). The NHL 94 disassembly (MarkeyJester, 2016)
builds with asm68k, whose `/p` listing rows are

    AAAAAAAA BBBB BBBB BBBB BBBB BBBB+  <label:>	<mnemonic>	<operands>

with an 8-digit address, up to five byte-words (a trailing `+` means more
follow), and the source text from column 36. Forward-referenced operands show
as `0000 0000` in pass-1 bytes, so byte values are never taken from the
listing; only the assembler's address / mnemonic decisions are. Table entries
are read from the verified ROM.

The ROM is built from two separately assembled parts:
  * Source.asm                     -> bytes $000000-$0FFABF
  * Common Library/Checksum/Source -> the 80-byte checksum stub at $0FFAC0
Both are assembled here into a scratch directory (the disassembly tree is never
written to), verified byte-for-byte against the supplied ROM, and merged.

Outputs (written into --out-dir, normally game/):
  nhl94.code_addrs.txt          every instruction-start address (code oracle)
  nhl94.disasm_labels.toml      [functions].extra = sub_/named code labels,
                                [functions].extra_seeds = loc_/locret_ interior labels
  nhl94.disasm_jumptables.toml  [[jump_table]] records for register-indexed dispatch
  annotations_from_disasm.csv   addr,name, for human-named code labels

Run:
  python tools/nhl94_disassembly.py --rom game/NHL94.bin
  python tools/nhl94_disassembly.py --rom game/NHL94.bin --reuse   # skip reassembly
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_DISASM = Path(r"C:\_Personal\NHL94Sandbox\GENS\GENS - NHL94 Disassembly\NHL94 Disassembly")
CHECKSUM_BASE = 0x0FFAC0          # where PatchRom.exe places the checksum stub

ROW_RE = re.compile(r"^([0-9A-F]{8}) (.{27})(.*)$")
LABEL_RE = re.compile(r"^([A-Za-z_.@][\w.@]*):")
HEXBYTES_RE = re.compile(r"^[0-9A-F]{2,4}( [0-9A-F]{2,4})*\+?$")
DATA_DIRECTIVES = {
    "dc.b", "dc.w", "dc.l", "dcb.b", "dcb.w", "dcb.l", "ds.b", "ds.w", "ds.l",
    "even", "align", "cnop", "org", "include", "binclude", "incbin", "rept",
    "endr", "macro", "endm", "equ", "set", "=", "obj", "objend", "section",
}
# Assembler-generated / anonymous names that are not human annotations.
GENERATED_NAME_RE = re.compile(
    r"^(sub|loc|locret|ptr|j|byte|word|dword|off|unk|asc|a)_?[0-9A-Fa-f]*$|^a[A-Z]\w*$"
)
INTERIOR_NAME_RE = re.compile(r"^(loc|locret)_[0-9A-Fa-f]+$")

# Register-indexed dispatch through a table whose base is a static symbol:
#   lea    TBL(pc),aN ; move.w (aN,dM.w),dM ; jsr (aN,dM.w)     word offsets
#   lea    TBL(pc),aN ; add.w  (aN,dM.w),aN ; jsr/jmp (aN)      word offsets
#   move.l #TBL,aN    ; move.l (aN,dM.w),aN ; jsr/jmp (aN)      absolute longs
# The finder only enumerates the PC-relative forms of these idioms, so the
# tables are declared as [[jump_table]] records (targets = base + word for
# "pcrel16", raw longwords for "abs"). Bounds: entries are read while each
# target is a known instruction start, stopping at the next labelled address
# or the first instruction start (handlers usually follow the table directly).
LEA_PC_RE = re.compile(r"^lea (\w+)\(pc\),a(\d)$")
MOVL_IMM_RE = re.compile(r"^move\.l #(\w+),a(\d)$")
IDX_W_RE = re.compile(r"^(?:move\.w|add\.w) \(a(\d),d(\d)\.w\),(?:d\d|a\d)$")
IDX_L_RE = re.compile(r"^move\.l \(a(\d),d(\d)\.w\),a(\d)$")
CALL_RE = re.compile(r"^(?:jsr|jmp) \(a(\d)(?:,d\d\.w)?\)$")


def run_asm68k(disasm_dir: Path, source_dir: Path, out_bin: Path, out_lst: Path) -> None:
    asm = disasm_dir / "_Assembly Tools" / "Asm68k.exe"
    if not asm.exists():
        sys.exit(f"asm68k not found: {asm}")
    # asm68k takes a single comma-separated argument list; pass the command
    # line as one string so Windows hands it over verbatim.
    cmd = f'"{asm}" /q /p Source.asm, "{out_bin}", , "{out_lst}"'
    r = subprocess.run(cmd, cwd=str(source_dir), capture_output=True, text=True)
    if r.returncode != 0 or not out_bin.exists():
        sys.exit(f"asm68k failed in {source_dir}:\n{r.stdout}\n{r.stderr}")


def verify(rom: bytes, built: bytes, base: int, upto: int | None, what: str) -> None:
    span = built if upto is None else built[:upto]
    ref = rom[base:base + len(span)]
    if span != ref:
        first = next(i for i in range(len(span)) if span[i] != ref[i])
        sys.exit(f"{what}: reassembled bytes differ from the ROM at ${base + first:06X}; "
                 "refusing to trust the listing")
    print(f"[verify] {what}: {len(span)} bytes at ${base:06X} match the ROM")


def parse_listing(path: Path, base: int, labels: dict[int, str],
                  code: set[int], data: set[int], src_of: dict[int, str],
                  pointer_refs: dict[str, list[int]],
                  pointer_addr_refs: dict[int, list[int]]) -> None:
    with open(path, encoding="latin-1") as f:
        for line in f:
            line = line.rstrip("\r\n")
            m = ROW_RE.match(line)
            if not m:
                continue
            addr = int(m.group(1), 16) + base
            bytes_col = m.group(2).strip()
            src = m.group(3).strip()
            if not src or src.startswith(";"):
                continue
            lm = LABEL_RE.match(src)
            if lm:
                labels.setdefault(addr, lm.group(1))
                src = src[lm.end():].strip()
            if not bytes_col or bytes_col.startswith("="):
                continue                      # equate or label-only row
            if not HEXBYTES_RE.match(bytes_col):
                continue
            if addr in code or addr in data:
                continue                      # first emit per address decides
            mnemonic = src.split(None, 1)[0].lower() if src else ""
            if not mnemonic or mnemonic in DATA_DIRECTIVES:
                data.add(addr)
                if mnemonic == "dc.l":
                    # Longword pointers in data: `dc.l loc_9A2A` inside a menu
                    # table is a handler the game later reaches through
                    # `jsr (a0)`; record the symbol so code targets become
                    # function entries even when their label is a `loc_`.
                    # A raw `dc.l $171CE` is the same idiom where IDA gave the
                    # target no label (it lands mid-function); resolve those
                    # numerically against the code set later.
                    for tok in src[4:].split(";", 1)[0].split(","):
                        tok = tok.strip()
                        if re.match(r"^[A-Za-z_]\w*$", tok):
                            pointer_refs.setdefault(tok, []).append(addr)
                        elif re.match(r"^\$[0-9A-Fa-f]+$", tok):
                            pointer_addr_refs.setdefault(int(tok[1:], 16), []).append(addr)
            else:
                code.add(addr)
                src_of[addr] = src


def norm(src: str) -> str:
    """Canonical one-space form of an instruction: `lea word_117b2(pc),a2`."""
    s = src.split(";", 1)[0].strip().lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"\s*,\s*", ",", s)
    return s


def find_jump_tables(rom: bytes, code: set[int], labels: dict[int, str],
                     src_of: dict[int, str]) -> list[tuple[int, int, int, str, str]]:
    by_name = {n.lower(): a for a, n in labels.items()}
    label_addrs = sorted(labels)
    addrs = sorted(src_of)
    out: list[tuple[int, int, int, str, str]] = []
    seen: set[int] = set()
    for i in range(len(addrs) - 2):
        s0, s1 = (norm(src_of[x]) for x in addrs[i:i + 2])
        m_lea, m_mov = LEA_PC_RE.match(s0), MOVL_IMM_RE.match(s0)
        m0 = m_lea or m_mov
        if not m0:
            continue
        base = by_name.get(m0.group(1).lower())
        if base is None or base in seen:
            continue
        reg = m0.group(2)
        m1w, m1l = IDX_W_RE.match(s1), IDX_L_RE.match(s1)
        if m_lea and m1w and m1w.group(1) == reg:
            fmt, stride, call_reg = "pcrel16", 2, reg
        elif m_mov and m1l and m1l.group(1) == reg:
            fmt, stride, call_reg = "abs", 4, m1l.group(3)
        else:
            continue
        # The indirect call may follow after a few unrelated instructions
        # (ObjListMaybe: `jsr sub_13040` sits between the load and `jsr (a0)`).
        m2 = None
        for k in range(2, 6):
            if i + k >= len(addrs):
                break
            sk = norm(src_of[addrs[i + k]])
            m2 = CALL_RE.match(sk)
            if m2 and m2.group(1) == call_reg:
                call_at = addrs[i + k]
                break
            m2 = None
            if re.search(r",a%s$" % call_reg, sk):    # register clobbered first
                break
        if not m2:
            continue
        next_label = next((x for x in label_addrs if x > base), len(rom))
        end = base
        while end + stride <= next_label and end + stride <= len(rom) and end not in code:
            if stride == 2:
                target = base + int.from_bytes(rom[end:end + 2], "big")
            else:
                target = int.from_bytes(rom[end:end + 4], "big")
            if target not in code:
                break
            end += stride
        if end > base:
            seen.add(base)
            out.append((base, end, stride, fmt,
                        f"{labels[base]} ({(end - base) // stride} entries) dispatched at ${call_at:06X}"))
    return out


def load_ida_names(xml_path: Path, code: set[int]) -> dict[int, tuple[str, str]]:
    """Human function names (and the end-of-line comment at the entry, if any)
    from an IDA Pro XML export (File > Produce > XML). Only FUNCTIONS entries
    with a non-generated name are used, and only at addresses the listing
    proves to be instruction starts; anything else is reported and skipped.
    The XML is the owner's current database, so its names win over the 2016
    listing's where both exist."""
    import xml.etree.ElementTree as ET
    root = ET.parse(xml_path).getroot()
    comments = {}
    cm = root.find("COMMENTS")
    if cm is not None:
        for c in cm:
            try:
                comments[int(c.attrib["ADDRESS"], 16)] = (c.text or "").strip()
            except (KeyError, ValueError):
                pass
    names: dict[int, tuple[str, str]] = {}
    skipped = []
    fn = root.find("FUNCTIONS")
    for f in (fn if fn is not None else []):
        name = f.attrib.get("NAME", "")
        try:
            addr = int(f.attrib["ENTRY_POINT"], 16)
        except (KeyError, ValueError):
            continue
        if not name or GENERATED_NAME_RE.match(name) or name.startswith(".") or name.startswith("nullsub_"):
            continue
        if addr not in code:
            skipped.append((addr, name))
            continue
        note = comments.get(addr, "").replace('"', "'").replace(",", ";").replace("\n", " ")
        names[addr] = (name, note)
    if skipped:
        print(f"[ida] {len(skipped)} named functions skipped (not instruction starts in the listing): "
              + ", ".join(f"${a:06X} {n}" for a, n in skipped[:8]))
    return names


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rom", type=Path, required=True, help="NHL94.bin to verify against")
    ap.add_argument("--disasm-dir", type=Path, default=DEFAULT_DISASM)
    ap.add_argument("--out-dir", type=Path,
                    default=Path(__file__).resolve().parents[1] / "game")
    ap.add_argument("--scratch", type=Path,
                    default=Path(tempfile.gettempdir()) / "nhl94_disasm_build")
    ap.add_argument("--reuse", action="store_true", help="reuse listings already in --scratch")
    ap.add_argument("--ida-xml", type=Path,
                    default=Path(__file__).resolve().parents[1] / "game" / "nhl94.xml",
                    help="IDA Pro XML export supplying function names (skipped if absent)")
    args = ap.parse_args()

    rom = args.rom.read_bytes()
    if len(rom) != 0x100000:
        sys.exit(f"unexpected ROM size {len(rom)}")
    args.scratch.mkdir(parents=True, exist_ok=True)
    main_bin, main_lst = args.scratch / "main.bin", args.scratch / "main.lst"
    chk_bin, chk_lst = args.scratch / "checksum.bin", args.scratch / "checksum.lst"

    if not (args.reuse and main_lst.exists() and chk_lst.exists()):
        run_asm68k(args.disasm_dir, args.disasm_dir, main_bin, main_lst)
        run_asm68k(args.disasm_dir, args.disasm_dir / "Common Library" / "Checksum",
                   chk_bin, chk_lst)
    verify(rom, main_bin.read_bytes(), 0, CHECKSUM_BASE, "Source.asm")
    verify(rom, chk_bin.read_bytes(), CHECKSUM_BASE, None, "Checksum stub")

    labels: dict[int, str] = {}
    code: set[int] = set()
    data: set[int] = set()
    src_of: dict[int, str] = {}
    pointer_refs: dict[str, list[int]] = {}
    pointer_addr_refs: dict[int, list[int]] = {}
    parse_listing(main_lst, 0, labels, code, data, src_of, pointer_refs, pointer_addr_refs)
    parse_listing(chk_lst, CHECKSUM_BASE, labels, code, data, src_of, pointer_refs, pointer_addr_refs)
    code = {a for a in code if a < len(rom)}
    tables = find_jump_tables(rom, code, labels, src_of)

    code_labels = {a: n for a, n in labels.items() if a in code}
    entries = {a: n for a, n in code_labels.items()
               if not INTERIOR_NAME_RE.match(n) and not n.startswith(".") and n[0] not in "+-"}
    # A code label stored as a longword pointer in data is dispatched through
    # at run time (menu handler tables), so it is an entry regardless of name.
    pointer_targets = {}
    for a, n in code_labels.items():
        if a not in entries and n in pointer_refs:
            entries[a] = n
            pointer_targets[a] = pointer_refs[n]
    # Unlabelled code address stored as a raw longword (`dc.l $171CE`, the
    # "Set Original lines" menu handler, which starts mid-way through
    # sub_171BE): equally an entry. Give it a synthetic name.
    for a, refs in pointer_addr_refs.items():
        if a in code and a not in entries:
            entries[a] = labels.get(a, f"ptr_{a:X}")
            pointer_targets[a] = refs
    seeds = {a: n for a, n in code_labels.items() if a not in entries}
    named = {a: (n, "") for a, n in entries.items() if not GENERATED_NAME_RE.match(n)}
    ida_count = 0
    if args.ida_xml and args.ida_xml.exists():
        ida = load_ida_names(args.ida_xml, code)
        named.update(ida)          # the owner's IDA names override the 2016 listing's
        ida_count = len(ida)
        print(f"[ida] {ida_count} function names from {args.ida_xml.name}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    nl = "\n"
    (args.out_dir / "nhl94.code_addrs.txt").write_text(
        "".join(f"{a:06X}{nl}" for a in sorted(code)), encoding="utf-8", newline=nl)

    lines = [
        "# nhl94.disasm_labels.toml - auto-generated by tools/nhl94_disassembly.py",
        "# from the byte-verified asm68k listing of the NHL 94 disassembly.",
        "#   [functions].extra       = sub_/named code labels (function-entry candidates)",
        "#   [functions].extra_seeds = loc_/locret_ interior labels (CFG-walk seeds)",
        "# Labels whose first assembled line is a data directive are omitted.",
        f"# Code labels: {len(entries)} entries, {len(seeds)} seeds; data labels skipped: "
        f"{len(labels) - len(code_labels)}",
        "",
        "[functions]",
        "extra = [",
    ]
    lines += [f"    0x{a:06X},   # {n}" + (f"  (pointer at ${pointer_targets[a][0]:06X})" if a in pointer_targets else "")
              for a, n in sorted(entries.items())]
    lines += ["]", "extra_seeds = ["]
    lines += [f"    0x{a:06X},   # {n}" for a, n in sorted(seeds.items())]
    lines += ["]", ""]
    (args.out_dir / "nhl94.disasm_labels.toml").write_text(nl.join(lines), encoding="utf-8", newline=nl)

    jt = [
        "# nhl94.disasm_jumptables.toml - auto-generated by tools/nhl94_disassembly.py.",
        "# Register-indexed dispatch tables with static bases found in the listing",
        "# (lea TBL(pc),aN / move.l #TBL,aN followed by an indexed jsr/jmp). Entries",
        "# were read from the ROM and each target verified as an instruction start.",
        f"# Tables: {len(tables)}",
        "",
    ]
    for base, end, stride, fmt, note in tables:
        jt += ["[[jump_table]]", f"start  = 0x{base:06X}", f"end    = 0x{end:06X}",
               f"stride = {stride}", f'format = "{fmt}"   # {note}', ""]
    (args.out_dir / "nhl94.disasm_jumptables.toml").write_text(nl.join(jt), encoding="utf-8", newline=nl)

    csv = ["# addr,name,notes - function names for the generated C. Names come from the",
           "# IDA Pro export game/nhl94.xml (FUNCTIONS with a human name, entry comment as",
           "# notes), falling back to the MarkeyJester 2016 listing's named labels.",
           "# Regenerate with tools/nhl94_disassembly.py (rerun after every IDA export)."]
    csv += [f"{a:06X},{n},\"{note}\"" if note else f"{a:06X},{n}," for a, (n, note) in sorted(named.items())]
    (args.out_dir / "annotations_from_disasm.csv").write_text(nl.join(csv) + nl, encoding="utf-8", newline=nl)

    print(f"[out] {len(code)} code addrs, {len(data)} data addrs")
    print(f"[out] {len(tables)} jump tables: " + ", ".join(f"${b:06X}/{f}" for b, _, _, f, _ in tables))
    print(f"[out] {len(entries)} entry labels ({len(pointer_targets)} promoted as data-pointer targets), "
          f"{len(seeds)} interior seeds, {len(named)} named annotations")
    print(f"[out] written to {args.out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
