#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=UTC
export LEAN_NUM_THREADS=1

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LEAN_PROJECT="$ROOT/Formalizations/Lean"
TARGET="$ROOT/Stage1_Instances/THM-M-0450"
LEAN_BIN=$(cd "$LEAN_PROJECT" && timeout 30s lake env which lean)
LEAN_DEPS=$(cd "$LEAN_PROJECT" && timeout 30s lake env printenv LEAN_PATH)
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-0450-proof.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

cp "$TARGET/Statement.lean" "$TMP/Statement.lean"
cp "$TARGET/ObligationTree.lean" "$TMP/ObligationTree.lean"
cp "$TARGET/Proof.lean" "$TMP/Proof.lean"

cd "$TMP"
LEAN_PATH="$LEAN_DEPS" timeout 120s "$LEAN_BIN" -o Statement.olean Statement.lean >statement.log 2>&1
LEAN_PATH=".:$LEAN_DEPS" timeout 120s "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean >tree.log 2>&1
LEAN_PATH=".:$LEAN_DEPS" timeout 120s "$LEAN_BIN" -o Proof.olean Proof.lean >proof.log 2>&1

python3 - proof.log <<'PY'
import re
import sys
from pathlib import Path

expected = {
    "Stage1Instances.THM_M_0450.Proof.fg_iff_of_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.finiteIndex_iff_of_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.comap_doubling_range",
    "Stage1Instances.THM_M_0450.Proof.doubling_finiteIndex_iff_of_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.northcott_comp_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.nonnegative_comp_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.parallelogram_comp_addEquiv",
    "Stage1Instances.THM_M_0450.Proof.jacobian_fg_iff_affine_fg",
    "Stage1Instances.THM_M_0450.Proof.jacobian_doubling_finiteIndex_iff_affine",
    "Stage1Instances.THM_M_0450.Proof.exactTarget_of_descent_packages",
}
text = Path(sys.argv[1]).read_text()
reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", text, re.DOTALL)
if {name for name, _ in reports} != expected:
    raise SystemExit("proof replay failed: declaration axiom-report coverage mismatch")
for name, raw_axioms in reports:
    axioms = [part.strip() for part in raw_axioms.split(",")]
    if axioms != ["propext", "Classical.choice", "Quot.sound"]:
        raise SystemExit(f"proof replay failed: unexpected axioms for {name}: {axioms}")
PY

if rg -n '\b(sorry|admit|sorryAx)\b|^[[:space:]]*(axiom|unsafe)[[:space:]]' "$TARGET/Proof.lean"; then
  echo "proof replay failed: prohibited proof device" >&2
  exit 1
fi

python3 "$TARGET/check_proof.py"
cat proof.log
echo "PASS THM-M-0450 pinned proof replay: 10 declarations, exact recorded axiom set"
