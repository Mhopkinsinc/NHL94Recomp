#!/bin/sh
# Apply one names batch, regenerate review/dossier/CSV, commit and push, then dump the next candidates.
# usage: _batch_cycle.sh NN "commit subject" [ndump]
set -e
cd /c/_Personal/NHL94Recomp
NN=$1; SUBJ=$2; ND=${3:-14}
python tools/nhl94_names.py apply game/names-batch-$NN.toml
python tools/nhl94_names.py review game/names-batch-$NN.toml
python tools/nhl94_names.py dossier
python tools/nhl94_disassembly.py --rom game/NHL94.bin --reuse 2>&1 | grep -E "named annotations"
python tools/nhl94_names.py status | tail -3
git add -A game docs
git -c core.safecrlf=false commit -q -F - <<EOF
$SUBJ

AI name proposals; review document, dossier and annotations CSV regenerated.

Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>
EOF
git push -q origin master 2>&1 | grep -v "^remote:" || true
git log --oneline -1
echo "=================== NEXT CANDIDATES ==================="
python - <<EOF
import re,sys; sys.path.insert(0,'tools'); import nhl94_names as N
d=open('game/nhl94.dossier.md',encoding='utf-8').read()
addrs=[int(m.group(1),16) for m in re.finditer(r'^## \\\$([0-9A-F]{6})',d,re.M)][:$ND]
ev=N.collect_evidence()
for a in addrs:
    print(f"===== \${a:06X} size={ev['size'][a]} callers={sorted(ev['nm'](c) for c in ev['callers'][a])}")
    if ev['strings'][a]: print("strings:", ev['strings'][a][:6])
    if ev['ramrefs'][a]: print("ram:", sorted(ev['ramrefs'][a]))
    for l in N.listing_body(a, ev['ext'], max_lines=28): print(l)
EOF
