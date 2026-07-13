#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0030"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" -o Statement.olean Statement.lean > statement.out 2>&1
LEAN_PATH=".:$lean_path" "$lean_bin" -o ObligationTree.olean ObligationTree.lean > obligation-tree.out
LEAN_PATH=".:$lean_path" "$lean_bin" Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = [
    "Ideal.iInf_pow_eq_bot_of_isLocalRing",
    "Ideal.iInf_pow_smul_eq_bot_of_isLocalRing",
    "Ideal.iInf_pow_smul_eq_bot_of_le_jacobson",
    "Ideal.mem_iInf_smul_pow_eq_bot_iff",
    "Stage1Instances.THM_M_0030.Proof.exactMathlibAnchor",
    "Stage1Instances.THM_M_0030.Proof.finiteModuleIntersection",
    "Stage1Instances.THM_M_0030.Proof.jacobsonIntersection",
    "Stage1Instances.THM_M_0030.Proof.properToMaximal",
    "Stage1Instances.THM_M_0030.Proof.maximalToJacobson",
    "Stage1Instances.THM_M_0030.Proof.jacobsonUnitSource",
    "Stage1Instances.THM_M_0030.Proof.fixedPointCharacterization",
    "Stage1Instances.THM_M_0030.Proof.fixedPointForward",
    "Stage1Instances.THM_M_0030.Proof.fixedPointBackward",
    "Stage1Instances.THM_M_0030.Proof.localProperIdealJacobson",
    "Stage1Instances.THM_M_0030.Proof.jacobsonUnit",
    "Stage1Instances.THM_M_0030.Proof.fixedPointCharacterization_via_branches",
    "Stage1Instances.THM_M_0030.Proof.jacobsonIntersection_via_frozen_composition",
    "Stage1Instances.THM_M_0030.Proof.finiteModuleIntersection_via_frozen_composition",
    "Stage1Instances.THM_M_0030.Proof.exactMathlibAnchor_via_frozen_composition",
    "Stage1Instances.THM_M_0030.Proof.krullIntersection_direct",
    "Stage1Instances.THM_M_0030.Proof.krullIntersection_via_pinned_anchor",
    "Stage1Instances.THM_M_0030.Proof.krullIntersection_via_frozen_composition",
]
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == 9
assert "sorryAx" not in output
PY
