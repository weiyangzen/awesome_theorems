#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m0012-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0012/{Statement,ObligationTree,Proof}.lean "$tmp/"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0012.Proof.fundamentalTheoremOfAlgebra",
    "Stage1Instances.THM_M_0012.Proof.fundamentalTheoremOfAlgebra_via_frozen_composition",
    "Complex.exists_root",
    "Stage1Instances.THM_M_0012.Proof.nonconstantDegreeBridge",
    "Stage1Instances.THM_M_0012.Proof.reciprocalDifferentiability",
    "Stage1Instances.THM_M_0012.Proof.reciprocalDecay",
    "Stage1Instances.THM_M_0012.Proof.liouvilleZero",
    "Stage1Instances.THM_M_0012.Proof.polynomialConstant",
    "Stage1Instances.THM_M_0012.Proof.noRootContradiction",
    "Stage1Instances.THM_M_0012.Proof.positiveDegreeAnchor_expanded",
    "Stage1Instances.THM_M_0012.Proof.positiveDegreeAnchor_mathlib",
    "Stage1Instances.THM_M_0012.Proof.fundamentalTheoremOfAlgebra_via_pinned_composition",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]", output, re.DOTALL
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",")}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
PY
