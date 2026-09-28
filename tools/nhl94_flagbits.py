"""nhl94_flagbits.py - every bset/bclr/btst/bchg on a WRAM flag word, grouped
by bit, with the enclosing routine and IDA comment, plus a few lines of
context around each set/clear site. Input for docs/GAMEFLAGS.md.

  python tools/nhl94_flagbits.py C2EC C2EE ...      (WRAM low words)
"""
import re, sys, bisect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import nhl94_names as N

ev = N.collect_evidence(); x = ev["text"]
funcs = sorted((a, n or f"sub_{a:X}") for a, n, _ in N.functions(x)); faddr = [a for a, _ in funcs]
def owner(a):
    i = bisect.bisect_right(faddr, a) - 1
    return funcs[i][1] if i >= 0 else "?"
cm = {int(m.group(1), 16): m.group(2).strip() for m in re.finditer(r'<COMMENT ADDRESS="0x([0-9A-Fa-f]+)"[^>]*>([^<]*)<', x)}
syms = {int(m.group(1), 16): m.group(2) for m in re.finditer(r'<SYMBOL ADDRESS="0x([0-9A-Fa-f]+)" NAME="([^"]+)"', x)}
row = re.compile(r"^([0-9A-F]{8}) (.{27})(.*)$")
rows = {}
for line in open(N.LISTING, encoding="latin-1"):
    m = row.match(line.rstrip("\r\n"))
    if m and m.group(2).strip():
        rows.setdefault(int(m.group(1), 16), re.sub(r"\s*;.*$", "", m.group(3).strip()))
addrs = sorted(rows)

def ctx(a, before=3, after=2):
    i = bisect.bisect_left(addrs, a)
    for k in addrs[max(0, i - before): i + after + 1]:
        mark = ">>" if k == a else "  "
        print(f"      {mark} {k:06X}  {rows[k]:40} {cm.get(k, '')[:60]}")

for w in sys.argv[1:]:
    word = "FFFF" + w.upper()
    full = 0xFF0000 | int(w, 16)
    print(f"\n######## ${w.upper()}  sym={syms.get(full, '-')}  cmt={cm.get(full, '')[:120]!r}")
    bybit = {}
    for a in addrs:
        src = rows[a]
        if word not in src:
            continue
        bm = re.match(r"(bset|bclr|btst|bchg)\s+#(\d+)", src)
        bit = int(bm.group(2)) if bm else None
        op = bm.group(1) if bm else src.split()[0]
        bybit.setdefault(bit, []).append((a, op, src))
    for bit in sorted(bybit, key=lambda b: (b is None, b)):
        uses = bybit[bit]
        setters = [u for u in uses if u[1] in ("bset", "bclr", "bchg")]
        testers = [u for u in uses if u[1] == "btst"]
        others = [u for u in uses if u[1] not in ("bset", "bclr", "bchg", "btst")]
        print(f"=== bit {bit}:  {len(setters)} set/clr, {len(testers)} tests")
        for a, op, src in setters:
            print(f"   {op} {a:06X} in {owner(a)}   {cm.get(a, '')[:70]}")
            ctx(a)
        if testers:
            names = {}
            for a, op, src in testers:
                names.setdefault(owner(a), []).append(f"{a:X}" + (f"({cm[a][:40]})" if cm.get(a) else ""))
            print("   tested in: " + "; ".join(f"{n} {','.join(v)}" for n, v in names.items()))
        for a, op, src in others:
            print(f"   {op} {a:06X} in {owner(a)}: {src}")
