#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/Stage1_Instances/THM-M-0958"
LEAN_ROOT="$ROOT/Formalizations/Lean"
LEAN_BIN=$(cd "$LEAN_ROOT" && lake env which lean)
LEAN_PATH=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)
TMP=$(mktemp -d /tmp/stage1-m0958-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

cp "$HERE/Statement.lean" "$TMP/Statement.lean"
cp "$HERE/Proof.lean" "$TMP/Proof.lean"

(
  cd "$TMP"
  LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH" "$LEAN_BIN" --trust=0 \
    -o Statement.olean Statement.lean >statement.log 2>&1
  LEAN_NUM_THREADS=1 LEAN_PATH=".:$LEAN_PATH" "$LEAN_BIN" --trust=0 \
    Proof.lean >proof.log 2>&1
)

test "$(grep -c "depends on axioms" "$TMP/proof.log")" -eq 9
test "$(grep -c "sorryAx" "$TMP/proof.log" || true)" -eq 0
test "$(grep -c "error:" "$TMP/proof.log" || true)" -eq 0
grep -q "Proof.digitEmbeddingPackage_checked.*depends on axioms" "$TMP/proof.log"
python3 - "$TMP/proof.log" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
blocks = re.findall(r"depends on axioms:\s*\[([^]]*)\]", text, flags=re.DOTALL)
assert len(blocks) == 9, len(blocks)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for block in blocks:
    observed = {item.strip() for item in block.replace("\n", " ").split(",") if item.strip()}
    assert observed <= allowed, observed
assert set().union(*(set(item.strip() for item in block.replace("\n", " ").split(",") if item.strip()) for block in blocks)) == allowed
PY

python3 "$HERE/check_proof.py"
printf '%s\n' "PASS S56-M-0958-PROOF: isolated trust=0 elaboration and evidence checks"
