#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m1005-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-1005/{Statement,ObligationTree,DoobLp,Proof}.lean "$tmp/"

lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -o "$tmp/DoobLp.olean" "$tmp/DoobLp.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1005.Proof.absSubmartingale",
    "Stage1Instances.THM_M_1005.Proof.measurable_runningAbsMax",
    "Stage1Instances.THM_M_1005.Proof.weakMaximal_abs",
    "MeasureTheory.maximal_ineq_Lp",
    "Stage1Instances.THM_M_1005.Proof.doobLpMomentEstimate",
    "Stage1Instances.THM_M_1005.Proof.doobLpMomentEstimate_via_frozen_composition",
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
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
print("PASS axiom reports: " + ", ".join(sorted(allowed)))
PY
