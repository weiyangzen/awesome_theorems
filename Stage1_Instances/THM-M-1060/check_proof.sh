#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=Asia/Shanghai
export LEAN_NUM_THREADS=1

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LEAN_PROJECT="$ROOT/Formalizations/Lean"
TARGET="$ROOT/Stage1_Instances/THM-M-1060"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-1060-proof.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

cd "$LEAN_PROJECT"
LEAN_BIN=$(lake env which lean)
LEAN_PATH_PINNED=$(lake env printenv LEAN_PATH)

version=$($LEAN_BIN --version)
case "$version" in
  *'version 4.29.0'*'commit 98dc76e3c0a9b856c9b98726b713fb04fab16740'*) ;;
  *) printf 'FAIL: unexpected Lean executable: %s\n' "$version" >&2; exit 1 ;;
esac

cp "$TARGET/Statement.lean" "$TARGET/Proof.lean" "$TMP"/
LEAN_PATH="$LEAN_PATH_PINNED" timeout --foreground --kill-after=10s 300s \
  "$LEAN_BIN" --trust=0 --root "$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean" \
  >"$TMP/statement.out" 2>&1
LEAN_PATH="$TMP:$LEAN_PATH_PINNED" timeout --foreground --kill-after=10s 300s \
  "$LEAN_BIN" --trust=0 --root "$TMP" "$TMP/Proof.lean" >"$TMP/proof.out" 2>&1
cat "$TMP/proof.out"

python3 - "$TMP/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1060.isProbabilityMeasure_of_isWienerMeasure",
    "Stage1Instances.THM_M_1060.measurableEvaluationLinear",
    "Stage1Instances.THM_M_1060.continuousScale",
    "Stage1Instances.THM_M_1060.zeroTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.zeroTimeLaw",
    "Stage1Instances.THM_M_1060.oneTimeVarianceAndLaw",
    "Stage1Instances.THM_M_1060.oneTimeLaw",
    "Stage1Instances.THM_M_1060.isGaussianProcess_of_isWienerMeasure",
)
allowed = ["propext", "Classical.choice", "Quot.sound"]
reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
by_name = {
    name: [part.strip() for part in raw.split(",") if part.strip()]
    for name, raw in reports
}
assert set(by_name) == set(declarations), (
    f"axiom-report coverage mismatch: expected={declarations}, actual={tuple(by_name)}"
)
for declaration in declarations:
    assert by_name[declaration] == allowed, (
        f"unexpected axiom closure for {declaration}: {by_name[declaration]}"
    )
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", output)
print("PASS THM-M-1060 trust-zero replay: eight partial proof bodies checked")
PY

printf '%s\n' \
  'closed frozen obligations: none; root remains open M4' \
  'proof_phase_complete=false; theorem_complete=false; accepted state unchanged'
