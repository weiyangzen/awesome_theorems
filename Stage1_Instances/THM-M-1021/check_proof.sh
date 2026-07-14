#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-1021"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/stage1-m1021-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$TMP/External/Bochner" "$TMP/Stage1_Instances/THM-M-1021"
cp "$TARGET/External/Bochner/PositiveDefinite.lean" "$TMP/External/Bochner/PositiveDefinite.lean"
cp "$TARGET/External/Bochner/FejerPD.lean" "$TMP/External/Bochner/FejerPD.lean"
cp "$TARGET/External/Bochner/Main.lean" "$TMP/External/Bochner/Main.lean"
cp "$TARGET/BochnerStatement.lean" "$TMP/Stage1_Instances/THM-M-1021/BochnerStatement.lean"
cp "$TARGET/Proof.lean" "$TMP/Stage1_Instances/THM-M-1021/Proof.lean"
cp "$TARGET/ProofAudit.lean" "$TMP/Stage1_Instances/THM-M-1021/ProofAudit.lean"

BASE_LEAN_PATH=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)
LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
export LEAN_NUM_THREADS=1

compile() {
  local module=$1
  local path="$TMP/${module}.lean"
  local olean="$TMP/${module}.olean"
  local output="$TMP/${module//\//-}.out"
  mkdir -p "$(dirname "$olean")"
  LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 600 "$LEAN" --trust=0 -t0 \
    -R "$TMP" -o "$olean" "$path" >"$output" 2>&1
}

compile External/Bochner/PositiveDefinite
compile External/Bochner/FejerPD
compile External/Bochner/Main
compile Stage1_Instances/THM-M-1021/BochnerStatement
compile Stage1_Instances/THM-M-1021/Proof

AUDIT_OUTPUT="$TMP/proof-audit.out"
LEAN_PATH="$TMP:$BASE_LEAN_PATH" timeout 600 "$LEAN" --trust=0 -t0 \
  -R "$TMP" "$TMP/Stage1_Instances/THM-M-1021/ProofAudit.lean" \
  >"$AUDIT_OUTPUT" 2>&1

python3 - "$AUDIT_OUTPUT" <<'PY'
import re
import sys
from pathlib import Path

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")

output = Path(sys.argv[1]).read_text(encoding="utf-8")
assert "error:" not in output
assert "sorryAx" not in output
assert output.count("Declarations are sorry-free!") == 4
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "bochner_theorem",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_forward",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_exact",
)
reports = re.findall(r"'([^']+)' depends on axioms: \[(.*?)]", output, re.DOTALL)
assert [name for name, _ in reports] == list(declarations), reports
for declaration, values in reports:
    actual = {name.strip() for name in values.split(",") if name.strip()}
    assert actual == allowed, f"unexpected axioms for {declaration}: {actual}"

print("PASS THM-M-1021 Lean proof: exact root elaborates; axioms match policy")
PY

python3 "$TARGET/check_proof.py"
