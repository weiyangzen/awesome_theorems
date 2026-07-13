#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../.." && pwd)"
LEAN_ROOT="$REPO_ROOT/Formalizations/Lean"
TMP="$(mktemp -d /tmp/stage1-m0995-validation.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT
umask 022

cp "$HERE"/{Statement,ObligationTree,Proof,Validation}.lean "$TMP/"

LEAN_BIN="${ELAN_HOME:-$HOME/.elan}/toolchains/leanprover--lean4---v4.29.0/bin/lean"
BASE_LEAN_PATH="$LEAN_ROOT/.lake/packages/Cli/.lake/build/lib/lean"
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible checkdecls mathlib flt-regular; do
  BASE_LEAN_PATH+=":$LEAN_ROOT/.lake/packages/$package/.lake/build/lib/lean"
done
BASE_LEAN_PATH+=":$LEAN_ROOT/.lake/build/lib/lean"
BASE_LEAN_PATH+=":${ELAN_HOME:-$HOME/.elan}/toolchains/leanprover--lean4---v4.29.0/lib/lean"
test -x "$LEAN_BIN"
test -f "$LEAN_ROOT/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/Moments/Variance.olean"

BASE=(
  bwrap --ro-bind / / --bind "$TMP" "$TMP" --dev /dev --proc /proc
  --unshare-net --die-with-parent --clearenv
  --setenv HOME "$TMP" --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 8 --chdir "$TMP"
)

run_lean() {
  local lean_path="$1"
  local log="$2"
  shift 2
  timeout 480 "${BASE[@]}" --setenv LEAN_PATH "$lean_path" \
    "$LEAN_BIN" --trust=0 "$@" >"$TMP/$log" 2>&1
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
    "Stage1Instances.THM_M_0995.ObligationTree.root_compose_v2",
    "Stage1Instances.THM_M_0995.ObligationTree.individualMGF_compose",
    "Stage1Instances.THM_M_0995.ObligationTree.sumMGF_compose",
    "Stage1Instances.THM_M_0995.ObligationTree.zeroVariance_compose",
    "Stage1Instances.THM_M_0995.Proof.bernsteinInequality_via_registry_v2",
    "Stage1Instances.THM_M_0995.Proof.bernsteinInequality",
    "Stage1Instances.THM_M_0995.Proof.not_optimizeExponentPackage",
    "Stage1Instances.THM_M_0995.Validation.exactRootViaRegistry",
    "Stage1Instances.THM_M_0995.Validation.exactRootDirect",
    "Stage1Instances.THM_M_0995.Validation.expandedRoot",
}
combined = "\n".join(Path(name).read_text(encoding="utf-8") for name in sys.argv[1:])
reports = {}
pattern = re.compile(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", re.DOTALL)
for declaration, body in pattern.findall(combined):
    reports[declaration] = {part.strip() for part in body.split(",") if part.strip()}
missing = expected - reports.keys()
assert not missing, f"missing axiom reports: {sorted(missing)}"
for declaration, observed in reports.items():
    assert observed <= allowed, f"unexpected axioms for {declaration}: {sorted(observed - allowed)}"
for declaration in expected:
    assert reports[declaration] == allowed, f"incomplete root/composition axiom set: {declaration}"
assert combined.count("Declarations are sorry-free!") == 3
assert "sorryAx" not in combined and "declaration uses 'sorry'" not in combined
assert "error:" not in combined
print(f"PASS axiom profile: {len(reports)} reports; exact roots and compositions use {sorted(allowed)}")
print("PASS validation adapters: three declarations are sorry-free")
PY

python3 "$HERE/check_proof_hygiene.py"
