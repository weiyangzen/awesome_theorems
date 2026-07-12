#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m0474-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0474/{Statement,ObligationTree,Proof}.lean "$tmp/"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$tmp/Proof.lean" | tee "$tmp/Proof.raw"
sed -E 's#^\./\.m0474-proof\.[^/]+/##' "$tmp/Proof.raw" > "$tmp/Proof.out"
test "$(grep -c 'Declarations are sorry-free!' "$tmp/Proof.out")" -eq 18
test "$(grep -c 'depends on axioms' "$tmp/Proof.out")" -eq 18
! grep -Eq 'warning:|error:|sorryAx' "$tmp/Proof.out"
python3 - "$tmp/Proof.out" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
blocks = re.findall(r"depends on axioms: \[(.*?)\]", text, flags=re.DOTALL)
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert len(blocks) == 18
for block in blocks:
    assert {name.strip() for name in block.split(",") if name.strip()} <= allowed
PY
