#!/usr/bin/env python3
"""nhl94_names.py - name the unnamed routines, with game/nhl94.xml as the source
of truth and a visible marker for machine-derived names.

Provenance rule
  Human names (from IDA) are plain:            NAME="getpde"
  AI-derived names carry the ai_ prefix and a  NAME="ai_PrintLineup"
  [AI] function comment with the evidence:     <REGULAR_CMT>[AI 0.8] ...</REGULAR_CMT>
  Accepting a name = dropping the prefix (in the XML or in IDA). The prefix
  shows up everywhere the name does: the XML, the annotations CSV, the
  generated C (`/* ai_PrintLineup */`), so nobody mistakes a guess for a fact.

Commands
  status                      counts: human / ai / unnamed functions
  dossier [--out FILE] [-n N] evidence table for the unnamed functions, priority order
                              (default output game/nhl94.dossier.md, tracked, regenerate per batch)
  review PROPOSALS.toml       reviewer's document for a batch: each proposal with its evidence,
                              callers/callees and the routine's assembly (docs/names/<batch>.md)
  apply PROPOSALS.toml        write ai_ names (+ evidence comments) into game/nhl94.xml;
                              entries with source = "listing" are human names from the
                              2016 listing and are written without the ai_ prefix
  accept ADDR [ADDR...]       drop the ai_ prefix (human confirmed) for those entries
  rename ADDR NAME --why ...  replace an existing (human or ai_) name; the old name is
                              kept in a [renamed, was X] comment together with the reason
  export-idc [--out FILE]     IDC script that applies the XML's ai_ names in IDA, if wanted

PROPOSALS.toml format (one table per routine):
  [[name]]
  addr = 0x00B4DE
  name = "PuckCollideStick"
  confidence = 0.8
  evidence = "called from updatepuck; reads puck struct $B74A and stick coords"

The XML is edited with minimal text changes (the FUNCTION line gains a NAME
attribute and a comment child) so diffs stay reviewable and IDA's XML import
still reads it.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
GAME = HERE.parent / "game"
XML = GAME / "nhl94.xml"
LISTING = Path(r"C:\Users\mhopkins\AppData\Local\Temp\nhl94lst\Listings.lst")

AI_PREFIX = "ai_"
PRINTERS = {"sub_11B92", "sub_11A36", "sub_11DE2", "sub_1172C", "printz", "print", "appstring", "appendz"}
HW = {
    "$C00000": "VDP data", "$C00004": "VDP ctrl", "$C00008": "HV counter",
    "$A10003": "pad1", "$A10005": "pad2", "$A11100": "Z80 busreq", "$A11200": "Z80 reset",
    "$A00000": "Z80 RAM", "$200000": "SRAM", "$A130F1": "SRAM ctrl",
}


# ---- XML access (text-level, to keep edits minimal) ----------------------------------
def read_xml() -> str:
    return XML.read_text(encoding="utf-8")


FUNC_RE = re.compile(r'^(\s*)<FUNCTION ENTRY_POINT="0x([0-9A-Fa-f]+)"((?: NAME="([^"]*)")?)\s*(/?)>', re.M)


def functions(text: str):
    """[(addr, name or None, match)] for every FUNCTION element."""
    out = []
    for m in FUNC_RE.finditer(text):
        out.append((int(m.group(2), 16), m.group(4) or None, m))
    return out


def xml_names(text: str) -> dict[int, str]:
    return {a: n for a, n, _ in functions(text) if n}


def symbol_names(text: str) -> dict[int, str]:
    d = {}
    for m in re.finditer(r'<SYMBOL ADDRESS="0x([0-9A-Fa-f]+)" NAME="([^"]*)"', text):
        d.setdefault(int(m.group(1), 16), m.group(2))
    return d


# ---- listing access ---------------------------------------------------------------------
ROW_RE = re.compile(r"^([0-9A-F]{8}) (.{27})(.*)$")


def load_listing():
    """rows: [(addr, src)] instruction rows; labels: addr -> label."""
    rows, labels = [], {}
    if not LISTING.exists():
        sys.exit(f"listing not found: {LISTING} (run tools/nhl94_disassembly.py first)")
    with open(LISTING, encoding="latin-1") as f:
        for line in f:
            m = ROW_RE.match(line.rstrip("\r\n"))
            if not m:
                continue
            addr = int(m.group(1), 16)
            src = m.group(3).strip()
            lm = re.match(r"^([A-Za-z_.][\w.]*):", src)
            if lm:
                labels.setdefault(addr, lm.group(1))
                src = src[lm.end():].strip()
            if not src or src.startswith(";") or not m.group(2).strip():
                continue
            mn = src.split(None, 1)[0].lower()
            if mn in ("dc.b", "dc.w", "dc.l", "dcb.b", "dcb.w", "dcb.l", "ds.b", "ds.w", "ds.l", "even", "align", "include", "incbin", "org"):
                continue
            rows.append((addr, src))
    return rows, labels


def function_extents(text: str) -> dict[int, tuple[int, int]]:
    ext = {}
    for m in re.finditer(r'<FUNCTION ENTRY_POINT="0x([0-9A-Fa-f]+)"[^>]*>\s*<ADDRESS_RANGE START="0x([0-9A-Fa-f]+)" END="0x([0-9A-Fa-f]+)"', text):
        ext[int(m.group(1), 16)] = (int(m.group(2), 16), int(m.group(3), 16))
    return ext


# ---- commands -------------------------------------------------------------------------------
def cmd_status(_args):
    text = read_xml()
    fs = functions(text)
    human = [a for a, n, _ in fs if n and not n.startswith(AI_PREFIX)]
    ai = [a for a, n, _ in fs if n and n.startswith(AI_PREFIX)]
    unnamed = [a for a, n, _ in fs if not n]
    print(f"functions in {XML.name}: {len(fs)}")
    print(f"  human-named : {len(human)}")
    print(f"  ai-named    : {len(ai)}   (ai_ prefix; accept with `accept ADDR`)")
    print(f"  unnamed     : {len(unnamed)}")
    return 0


def collect_evidence():
    """Static evidence for every function: callers, callees, strings, RAM, hw, size."""
    text = read_xml()
    names = xml_names(text)
    syms = symbol_names(text)
    ram = {a & 0xFFFF: n for a, n in syms.items() if a >= 0xFF0000}
    ext = function_extents(text)
    rows, labels = load_listing()
    # index instructions by function (XML ranges), then by listing label fallback
    fn_of = {}
    starts = sorted(ext)
    for a, _ in rows:
        # binary search the function whose range contains a
        lo, hi = 0, len(starts) - 1
        f = None
        while lo <= hi:
            mid = (lo + hi) // 2
            s, e = ext[starts[mid]]
            if a < s:
                hi = mid - 1
            elif a > e:
                lo = mid + 1
            else:
                f = starts[mid]; break
        if f is not None:
            fn_of[a] = f
    callers = defaultdict(set)
    callees = defaultdict(set)
    strings = defaultdict(list)
    ramrefs = defaultdict(set)
    hwrefs = defaultdict(set)
    size = defaultdict(int)
    call_re = re.compile(r"^(?:jsr|bsr\.?[sw]?|jmp|bra\.?[sw]?)\s+([A-Za-z_][\w]*)")
    for i, (a, src) in enumerate(rows):
        f = fn_of.get(a)
        if f is None:
            continue
        size[f] += 1
        m = call_re.match(src)
        if m:
            tgt = m.group(1)
            taddr = next((k for k, v in labels.items() if v == tgt), None) if tgt.startswith(("sub_", "loc_")) else None
            if taddr is None:
                taddr = {v: k for k, v in labels.items()}.get(tgt)
            if taddr is not None and taddr != f:
                callees[f].add(taddr)
                callers[taddr].add(f)
            # inline printer text: the dc.b string rows follow the jsr in the listing
            if tgt in PRINTERS or names.get(taddr, "") in PRINTERS:
                pass
        for hw, what in HW.items():
            if hw in src:
                hwrefs[f].add(what)
        for mm in re.finditer(r"\(\$FFFF([0-9A-F]{4})\)\.w", src):
            ra = int(mm.group(1), 16)
            if ra in ram:
                ramrefs[f].add(ram[ra])
    # inline strings: scan the raw listing for dc.b 'text' rows and attribute to the function of the preceding instruction
    with open(LISTING, encoding="latin-1") as fh:
        last_fn = None
        for line in fh:
            m = ROW_RE.match(line.rstrip("\r\n"))
            if not m:
                continue
            a = int(m.group(1), 16)
            src = m.group(3).strip()
            if a in fn_of:
                last_fn = fn_of[a]
            sm = re.search(r"dc\.b\s+'([^']{3,})'", src)
            if sm and last_fn is not None and a - ext.get(last_fn, (0, 0))[1] < 0x200:
                if len(strings[last_fn]) < 6:
                    strings[last_fn].append(sm.group(1).strip())

    def nm(a):
        return names.get(a) or labels.get(a) or f"${a:06X}"

    return dict(text=text, names=names, labels=labels, callers=callers, callees=callees,
                strings=strings, ramrefs=ramrefs, hwrefs=hwrefs, size=size, nm=nm, ext=ext)


def cmd_dossier(args):
    ev = collect_evidence()
    text, labels, callers, callees = ev["text"], ev["labels"], ev["callers"], ev["callees"]
    strings, ramrefs, hwrefs, size, nm = ev["strings"], ev["ramrefs"], ev["hwrefs"], ev["size"], ev["nm"]
    unnamed = [a for a, n, _ in functions(text) if not n]
    # priority: many distinct callers first, then size
    unnamed.sort(key=lambda a: (-len(callers[a]), -size[a]))
    if args.limit:
        unnamed = unnamed[: args.limit]
    out = []
    out.append("# Unnamed-routine dossier (auto-generated by tools/nhl94_names.py)")
    out.append("# columns: addr | insns | callers | callees | strings | named RAM | hardware")
    for a in unnamed:
        out.append(f"\n## ${a:06X}  ({labels.get(a, '?')}, {size[a]} insns, {len(callers[a])} callers)")
        out.append("callers : " + (", ".join(sorted(nm(c) for c in callers[a])) or "-"))
        out.append("callees : " + (", ".join(sorted(nm(c) for c in callees[a])) or "-"))
        if strings[a]:
            out.append("strings : " + " | ".join(strings[a]))
        if ramrefs[a]:
            out.append("ram     : " + ", ".join(sorted(ramrefs[a])))
        if hwrefs[a]:
            out.append("hw      : " + ", ".join(sorted(hwrefs[a])))
    result = "\n".join(out) + "\n"
    out_path = Path(args.out) if args.out else GAME / "nhl94.dossier.md"
    out_path.write_text(result, encoding="utf-8", newline="\n")
    print(f"wrote {out_path} ({len(unnamed)} routines)")
    return 0


def listing_body(addr: int, ext: dict, max_lines: int = 60) -> list[str]:
    """Assembly rows of the function at addr (XML extent, else until the next rts)."""
    lo, hi = ext.get(addr, (addr, addr + 0x400))
    body = []
    with open(LISTING, encoding="latin-1") as fh:
        for line in fh:
            m = ROW_RE.match(line.rstrip("\r\n"))
            if not m:
                continue
            a = int(m.group(1), 16)
            if a < lo:
                continue
            if a > hi:
                break
            src = m.group(3).strip()
            if not src or src.startswith(";") or not m.group(2).strip():
                continue
            src = re.sub(r"\s*;.*$", "", src)
            body.append(f"{a:06X}  {src}")
            if len(body) >= max_lines:
                body.append("...")
                break
    return body


def cmd_review(args):
    ev = collect_evidence()
    props = parse_proposals(Path(args.proposals))
    nm, callers, callees, strings, ramrefs, hwrefs, size, ext = (ev[k] for k in ("nm", "callers", "callees", "strings", "ramrefs", "hwrefs", "size", "ext"))
    batch = Path(args.proposals).stem.replace("nhl94.names.", "")
    out = [f"# Name review: {Path(args.proposals).name}", "",
           "For each routine: the proposed `ai_` name, confidence, the evidence the",
           "proposal rests on, who calls it and what it calls, and its assembly.",
           "Accept with `python tools/nhl94_names.py accept <addr>`; to rename, edit the",
           "XML (or the proposals file and re-apply).", ""]
    for addr, name, conf, evidence, source in props:
        shown = name if source == "listing" else f"ai_{name}"
        tag = "from the 2016 listing, not AI" if source == "listing" else f"confidence {conf:.1f}"
        out.append(f"## `${addr:06X}` -> `{shown}`  ({tag}, {size[addr]} insns)")
        out.append("")
        out.append(f"**Evidence.** {evidence}")
        out.append("")
        out.append("**Callers.** " + (", ".join(sorted(nm(c) for c in callers[addr])) or "none found"))
        out.append("**Callees.** " + (", ".join(sorted(nm(c) for c in callees[addr])) or "none"))
        if strings[addr]:
            out.append("**Strings.** " + " | ".join(strings[addr]))
        if ramrefs[addr]:
            out.append("**RAM.** " + ", ".join(sorted(ramrefs[addr])))
        if hwrefs[addr]:
            out.append("**Hardware.** " + ", ".join(sorted(hwrefs[addr])))
        out.append("")
        out.append("```")
        out += listing_body(addr, ext)
        out.append("```")
        out.append("")
    out_path = Path(args.out) if args.out else HERE.parent / "docs" / "names" / f"{batch}.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {out_path} ({len(props)} proposals)")
    return 0


def parse_proposals(path: Path):
    import tomllib
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    props = []
    for t in data.get("name", []):
        addr = int(t["addr"]) if not isinstance(t["addr"], str) else int(t["addr"], 16)
        name = t["name"].strip()
        if not re.match(r"^[A-Za-z_]\w*$", name):
            sys.exit(f"bad identifier {name!r} for {addr:06X}")
        source = t.get("source", "ai")
        if source not in ("ai", "listing"):
            sys.exit(f"bad source {source!r} for {addr:06X} (ai or listing)")
        props.append((addr, name, float(t.get("confidence", 0.5)), t.get("evidence", "").strip(), source))
    return props


def cmd_apply(args):
    text = read_xml()
    props = parse_proposals(Path(args.proposals))
    applied, skipped = 0, []
    for addr, name, conf, evidence, source in props:
        m = next((mm for a, n, mm in functions(text) if a == addr), None)
        if m is None:
            skipped.append((addr, "no FUNCTION at that address in the XML")); continue
        existing = m.group(4)
        if existing and not existing.startswith(AI_PREFIX):
            skipped.append((addr, f"human-named already ({existing})")); continue
        if source == "listing":      # human name from the 2016 listing: no ai_ prefix
            full = name
            cmt = f"[listing] {evidence}"
        else:
            full = name if name.startswith(AI_PREFIX) else AI_PREFIX + name
            cmt = f"[AI {conf:.1f}] {evidence}"
        indent = m.group(1)
        cmt = cmt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        if m.group(5) == "/":   # self-closing FUNCTION: expand it
            new_line = f'{indent}<FUNCTION ENTRY_POINT="0x{addr:X}" NAME="{full}">\n{indent}    <REGULAR_CMT>{cmt}</REGULAR_CMT>\n{indent}</FUNCTION>'
            text = text[: m.start()] + new_line + text[m.end():]
        else:
            head = f'{indent}<FUNCTION ENTRY_POINT="0x{addr:X}" NAME="{full}">'
            # replace the open tag, then insert/replace the [AI] comment right after ADDRESS_RANGE
            text = text[: m.start()] + head + text[m.end():]
            # find this element's end
            start = text.index(head)
            end = text.index("</FUNCTION>", start)
            body = text[start:end]
            body = re.sub(r"\n\s*<REGULAR_CMT>\[(AI|listing)[^<]*</REGULAR_CMT>", "", body)
            ins = body.find("/>", body.find("<ADDRESS_RANGE"))
            if ins >= 0:
                ins += 2
                body = body[:ins] + f"\n{indent}    <REGULAR_CMT>{cmt}</REGULAR_CMT>" + body[ins:]
            text = text[:start] + body + text[end:]
        applied += 1
    XML.write_text(text, encoding="utf-8", newline="\n")
    print(f"applied {applied} ai_ names to {XML.name}")
    for addr, why in skipped:
        print(f"  skipped ${addr:06X}: {why}")
    return 0


def cmd_accept(args):
    text = read_xml()
    n = 0
    for s in args.addrs:
        addr = int(s, 16)
        m = next((mm for a, nn, mm in functions(text) if a == addr), None)
        if m is None or not m.group(4) or not m.group(4).startswith(AI_PREFIX):
            print(f"  ${addr:06X}: no ai_ name to accept"); continue
        plain = m.group(4)[len(AI_PREFIX):]
        text = text[: m.start()] + f'{m.group(1)}<FUNCTION ENTRY_POINT="0x{addr:X}" NAME="{plain}">' + text[m.end():]
        text = re.sub(r"(ENTRY_POINT=\"0x%X\" NAME=\"%s\">\s*<ADDRESS_RANGE[^>]*/>)\n\s*<REGULAR_CMT>\[AI ([^\]]*)\]" % (addr, re.escape(plain)),
                      r"\1\n            <REGULAR_CMT>[accepted, was AI \2]", text)
        n += 1
    XML.write_text(text, encoding="utf-8", newline="\n")
    print(f"accepted {n} names")
    return 0


def cmd_rename(args):
    text = read_xml()
    addr = int(args.addr, 16)
    new = args.name.strip()
    if not re.match(r"^[A-Za-z_]\w*$", new):
        sys.exit(f"bad identifier {new!r}")
    m = next((mm for a, nn, mm in functions(text) if a == addr), None)
    if m is None:
        sys.exit(f"no FUNCTION at ${addr:06X}")
    old = m.group(4) or f"sub_{addr:X}"
    indent = m.group(1)
    head = f'{indent}<FUNCTION ENTRY_POINT="0x{addr:X}" NAME="{new}">'
    cmt = f"[renamed, was {old}] {args.why}".replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    if m.group(5) == "/":
        text = text[: m.start()] + f"{head}\n{indent}    <REGULAR_CMT>{cmt}</REGULAR_CMT>\n{indent}</FUNCTION>" + text[m.end():]
    else:
        text = text[: m.start()] + head + text[m.end():]
        start = text.index(head); end = text.index("</FUNCTION>", start)
        body = text[start:end]
        body = re.sub(r"\n\s*<REGULAR_CMT>\[(AI|listing|renamed)[^<]*</REGULAR_CMT>", "", body)
        ins = body.find("/>", body.find("<ADDRESS_RANGE"))
        if ins >= 0:
            ins += 2
            body = body[:ins] + f"\n{indent}    <REGULAR_CMT>{cmt}</REGULAR_CMT>" + body[ins:]
        text = text[:start] + body + text[end:]
    # the type-info comment and the SYMBOLS table carry the same name; keep them in step
    text = text.replace(f"<TYPEINFO_CMT>{old}</TYPEINFO_CMT>", f"<TYPEINFO_CMT>{new}</TYPEINFO_CMT>")
    text = re.sub(r'(<SYMBOL ADDRESS="0x%X" NAME=")%s(")' % (addr, re.escape(old)), r"\g<1>%s\g<2>" % new, text)
    XML.write_text(text, encoding="utf-8", newline="\n")
    print(f"renamed ${addr:06X}: {old} -> {new}")
    return 0


def cmd_export_idc(args):
    text = read_xml()
    lines = ["// Apply ai_ names from game/nhl94.xml in IDA (File > Script file).", "#include <idc.idc>", "static main() {"]
    for a, n, _ in functions(text):
        if n and n.startswith(AI_PREFIX):
            lines.append(f'  set_name(0x{a:X}, "{n}", SN_NOCHECK);')
    lines.append("}")
    out = Path(args.out) if args.out else GAME / "nhl94_ai_names.idc"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    d = sub.add_parser("dossier"); d.add_argument("--out"); d.add_argument("-n", "--limit", type=int, default=0)
    r = sub.add_parser("review"); r.add_argument("proposals"); r.add_argument("--out")
    a = sub.add_parser("apply"); a.add_argument("proposals")
    c = sub.add_parser("accept"); c.add_argument("addrs", nargs="+")
    rn = sub.add_parser("rename"); rn.add_argument("addr"); rn.add_argument("name"); rn.add_argument("--why", required=True)
    e = sub.add_parser("export-idc"); e.add_argument("--out")
    args = ap.parse_args()
    return {"status": cmd_status, "dossier": cmd_dossier, "review": cmd_review, "apply": cmd_apply, "accept": cmd_accept, "rename": cmd_rename, "export-idc": cmd_export_idc}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
