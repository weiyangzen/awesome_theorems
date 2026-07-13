#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=UTC
export LEAN_NUM_THREADS=1

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LEAN_PROJECT="$ROOT/Formalizations/Lean"
TARGET="$ROOT/Stage1_Instances/THM-M-1029"
TOOLCHAIN=$(tr -d '\r\n' < "$LEAN_PROJECT/lean-toolchain")
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-1029-proof.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

# Ask pinned mathlib's own Lake project to select the pinned Lean executable.
# Its nested dependency cache is source-only in this worker image, so compose
# the import path from the already materialized top-level compiled artifacts.
# This avoids traversing the unrelated top-level flt-regular dependency.
MATHLIB="$LEAN_PROJECT/.lake/packages/mathlib"
LEAN_BIN=$(cd "$MATHLIB" && timeout 60 lake env which lean)
LEAN_PATH_PARTS=()
while IFS= read -r path; do
  LEAN_PATH_PARTS+=("$path")
done < <(find -L "$LEAN_PROJECT/.lake/packages" -path '*/.lake/build/lib/lean' -type d -print | sort)
LEAN_PATH_PARTS+=("$(readlink -f "$LEAN_PROJECT/.lake")/build/lib/lean")
LEAN_PATH_PARTS+=("$(dirname "$LEAN_BIN")/../lib/lean")
BASE_LEAN_PATH=$(IFS=:; printf '%s' "${LEAN_PATH_PARTS[*]}")

run_lean() {
  local import_path=$1
  local output=$2
  local source=$3
  (cd "$MATHLIB" && timeout 600 lake env env \
    LEAN_NUM_THREADS="$LEAN_NUM_THREADS" LEAN_PATH="$import_path" \
    "$LEAN_BIN" --root="$TMP" --trust=0 -t0 -o "$output" "$TMP/$source")
}

cp "$TARGET"/{Statement,ObligationTree,Proof}.lean "$TMP/"

cd "$TMP"
run_lean "$BASE_LEAN_PATH" "$TMP/Statement.olean" Statement.lean >statement.log 2>&1
run_lean "$TMP:$BASE_LEAN_PATH" "$TMP/ObligationTree.olean" ObligationTree.lean >tree.log 2>&1
run_lean "$TMP:$BASE_LEAN_PATH" "$TMP/Proof.olean" Proof.lean >proof.log 2>&1

python3 - tree.log proof.log <<'PY'
import re
import sys
from pathlib import Path

allowed = ["propext", "Classical.choice", "Quot.sound"]
expected_tree = {
    "Stage1Instances.THM_M_1029.root_of_incrementLawPackage",
}
expected_proof = {
    "Stage1Instances.THM_M_1029.Proof.bracketCompensated_deterministicTime_eq",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_continuousPaths",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_monotonePaths",
    "Stage1Instances.THM_M_1029.Proof.deterministicTimeProcess_startsAtZero",
    "Stage1Instances.THM_M_1029.Proof.bracketCompensated_martingale_of_quadratic",
    "Stage1Instances.THM_M_1029.Proof.quadraticCompensated_stronglyAdapted",
    "Stage1Instances.THM_M_1029.Proof.square_stronglyAdapted",
    "Stage1Instances.THM_M_1029.Proof.deterministicTime_stronglyAdapted_of_martingales",
    "Stage1Instances.THM_M_1029.Proof.quadratic_coordinate_integrable",
    "Stage1Instances.THM_M_1029.Proof.coordinate_memLp_two",
    "Stage1Instances.THM_M_1029.Proof.increment_memLp_two",
    "Stage1Instances.THM_M_1029.Proof.increment_square_integrable",
    "Stage1Instances.THM_M_1029.Proof.increment_condExp_eq_zero",
    "Stage1Instances.THM_M_1029.Proof.increment_condExp_sq",
    "Stage1Instances.THM_M_1029.Proof.integral_process_eq_zero",
    "Stage1Instances.THM_M_1029.Proof.integral_process_sq_eq_time",
    "Stage1Instances.THM_M_1029.Proof.variance_process_eq_time",
    "Stage1Instances.THM_M_1029.Proof.zeroElapsedIncrement",
    "Stage1Instances.THM_M_1029.Proof.hasLaw_gaussianReal_of_charFun",
    "Stage1Instances.THM_M_1029.Proof.hasLaw_gaussianReal_zero",
    "Stage1Instances.THM_M_1029.Proof.incrementLawPackage_of_components",
    "Stage1Instances.THM_M_1029.Proof.incrementLawPackage_of_strict",
    "Stage1Instances.THM_M_1029.Proof.root_of_assumedIncrementComponents",
}


def check(path, expected):
    output = Path(path).read_text(encoding="utf-8")
    reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
    names = {name for name, _ in reports}
    if names != expected:
        raise SystemExit(
            f"proof replay failed: {path} axiom coverage mismatch: "
            f"missing={sorted(expected - names)}, extra={sorted(names - expected)}"
        )
    for name, raw in reports:
        axioms = [part.strip() for part in raw.split(",") if part.strip()]
        if axioms != allowed:
            raise SystemExit(f"proof replay failed: unexpected axioms for {name}: {axioms}")
    if "error:" in output:
        raise SystemExit(f"proof replay failed: Lean error in {path}")


check(sys.argv[1], expected_tree)
check(sys.argv[2], expected_proof)
PY

if rg -n --pcre2 \
    '\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern)[[:space:]]' \
    "$TARGET"/{Statement,ObligationTree,Proof}.lean; then
  echo "proof replay failed: prohibited proof device" >&2
  exit 1
fi

python3 -B "$TARGET/check_proof.py"
cat tree.log
cat proof.log
printf '%s\n' \
  'PASS THM-M-1029 pinned proof replay: 23 local bodies and the frozen conditional composition checked' \
  'root closure: open (M3); strict-positive increment Gaussianity and independence remain open'
