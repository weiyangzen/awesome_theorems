#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0957"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0957-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && timeout 300 lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean" \
  >"$tmp/obligation-tree.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" "$target/Proof.lean" \
  >"$tmp/proof.out" 2>&1

cat "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0957_ObligationTree.dimensionControl_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.rpowNormalization_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyRpowIdentity_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxySlackAbsorption_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.ambientFit_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearCeiling_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearIncrementAbsorption_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.dimensionSlack_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.logDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.reciprocalBalancedCore_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.reciprocalDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.radixNonzero_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.radixFloor_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.quantitativeConstruction_installed",
    "Stage1Instances.THM_M_0957_ObligationTree.indexMonotonicity_installed",
    "Stage1Instances.THM_M_0957_ObligationTree.parameterAdmissibility_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyLogLower_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.subleadingLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.optimalExponentBridge_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyAsymptotic_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.ratioAsymptotic_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.sharpEstimate_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.sharpParameter_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.exactRoot_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.behrendConstructionTarget_proof",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    no_axioms = f"'{declaration}' does not depend on any axioms" in output
    assert match or no_axioms, f"missing axiom report for {declaration}"
    if match:
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
PY

python3 -B "$target/check_proof.py"

printf '%s\n' \
  'PASS THM-M-0957 proof: exact historical root kernel-closed' \
  'proof-reachable obligations: 26; accepted obligations: 0 pending master acceptance' \
  'theorem completion: false; validation and release gates remain downstream'
