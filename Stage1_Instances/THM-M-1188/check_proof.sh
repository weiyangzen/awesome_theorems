#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d /tmp/m1188-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-1188/{Statement,ObligationTree,Proof}.lean "$tmp/"

lake env lean --trust=0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean --trust=0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
    "$tmp/ObligationTree.lean" >"$tmp/obligation-tree.out"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean --trust=0 -R "$tmp" "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/obligation-tree.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = "\n".join(Path(path).read_text(encoding="utf-8") for path in sys.argv[1:])
declarations = (
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
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",")}
    assert actual == allowed, f"unexpected axioms for {declaration}: {actual}"
assert "sorryAx" not in output
print("PASS exact proof and frozen composition axioms: " + ", ".join(sorted(allowed)))
PY
