#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
LEAN_ROOT="$REPO_ROOT/Formalizations/Lean"
TMP="$(mktemp -d /tmp/stage1-m1188-validation.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT
umask 022

cp "$HERE"/{Statement,ObligationTree,Proof,Validation}.lean "$TMP/"

ELAN_ROOT="${ELAN_HOME:-$HOME/.elan}"
LAKE_BIN="$ELAN_ROOT/bin/lake"
BASE_LEAN_PATH="$LEAN_ROOT/.lake/packages/Cli/.lake/build/lib/lean"
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible checkdecls mathlib flt-regular; do
  BASE_LEAN_PATH+=":$LEAN_ROOT/.lake/packages/$package/.lake/build/lib/lean"
done
BASE_LEAN_PATH+=":$LEAN_ROOT/.lake/build/lib/lean"
BASE_LEAN_PATH+=":$ELAN_ROOT/toolchains/leanprover--lean4---v4.29.0/lib/lean"
test -x "$LAKE_BIN"
test -f "$LEAN_ROOT/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Analysis/InnerProductSpace/Laplacian.olean"

BASE=(
  bwrap --ro-bind / / --bind "$TMP" "$TMP" --dev /dev --proc /proc
  --unshare-net --die-with-parent --clearenv
  --setenv HOME "$TMP" --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1
  --setenv ELAN_HOME "$ELAN_ROOT"
  --setenv ELAN_TOOLCHAIN leanprover/lean4:v4.29.0 --chdir "$TMP"
)

run_lean() {
  local lean_path="$1"
  local log="$2"
  shift 2
  timeout 540 "${BASE[@]}" --setenv LEAN_PATH "$lean_path" \
    "$LAKE_BIN" env lean --trust=0 "$@" >"$TMP/$log" 2>&1
}

run_lean "$BASE_LEAN_PATH" statement.log -o "$TMP/Statement.olean" Statement.lean
run_lean "$TMP:$BASE_LEAN_PATH" obligation.log -o "$TMP/ObligationTree.olean" ObligationTree.lean
run_lean "$TMP:$BASE_LEAN_PATH" proof.log -o "$TMP/Proof.olean" Proof.lean
run_lean "$TMP:$BASE_LEAN_PATH" validation.log Validation.lean

cat "$TMP"/{obligation,proof,validation}.log

python3 - "$TMP/obligation.log" "$TMP/proof.log" "$TMP/validation.log" <<'PY'
import re
import sys
from pathlib import Path

allowed = {"propext", "Classical.choice", "Quot.sound"}
expected = {
    "Stage1Instances.THM_M_1188.ObligationTree.root_compose",
    "Stage1Instances.THM_M_1188.Proof.closedCylinder_isCompact",
    "Stage1Instances.THM_M_1188.Proof.iteratedDeriv_two_nonpos_of_isLocalMax",
    "Stage1Instances.THM_M_1188.Proof.directional_second_eq",
    "Stage1Instances.THM_M_1188.Proof.laplacian_nonpos_of_isLocalMax",
    "Stage1Instances.THM_M_1188.Proof.closedCylinder_nonempty",
    "Stage1Instances.THM_M_1188.Proof.parabolicBoundary_isCompact",
    "Stage1Instances.THM_M_1188.Proof.parabolicBoundary_nonempty",
    "Stage1Instances.THM_M_1188.Proof.exists_closedCylinder_isMaxOn",
    "Stage1Instances.THM_M_1188.Proof.exists_parabolicBoundary_isMaxOn",
    "Stage1Instances.THM_M_1188.Proof.mem_frontier_of_mem_closure_not_mem",
    "Stage1Instances.THM_M_1188.Proof.mem_parabolicBoundary_of_time_eq_zero_or_not_mem",
    "Stage1Instances.THM_M_1188.Proof.deriv_nonneg_of_isMaxOn_Icc",
    "Stage1Instances.THM_M_1188.Proof.weak_maximum_principle",
    "Stage1Instances.THM_M_1188.Proof.heatEquationWeakMaximumPrinciple",
    "Stage1Instances.THM_M_1188.Proof.analyticMaximumEngine",
    "Stage1Instances.THM_M_1188.Proof.assembledObligationRoot",
    "Stage1Instances.THM_M_1188.Validation.exactCanonicalRoot",
    "Stage1Instances.THM_M_1188.Validation.exactComposedRoot",
}
combined = "\n".join(Path(name).read_text(encoding="utf-8") for name in sys.argv[1:])
reports = {}
pattern = re.compile(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", re.DOTALL)
for declaration, body in pattern.findall(combined):
    reports[declaration] = {part.strip() for part in body.split(",") if part.strip()}
missing = expected - reports.keys()
assert not missing, f"missing axiom reports: {sorted(missing)}"
for declaration in expected:
    assert reports[declaration] == allowed, (declaration, reports[declaration])
assert combined.count("Declarations are sorry-free!") == 2
assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
assert "error:" not in combined
print(f"PASS axiom profile: {len(reports)} reports; checked roots and composition use {sorted(allowed)}")
print("PASS same-worker exact-target validation adapters are sorry-free")
PY
