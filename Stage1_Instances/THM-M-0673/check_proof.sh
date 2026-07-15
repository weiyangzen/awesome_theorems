#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0673"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"

cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" --trust=0 -o Statement.olean Statement.lean \
  > statement.out 2>&1
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 -o ObligationTree.olean \
  ObligationTree.lean > obligation-tree.out 2>&1
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 Proof.lean | tee proof.out

python3 - proof.out <<'PY'
from pathlib import Path
import re
import sys

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = [
    "FirstOrder.Language.Ultraproduct.funMap_cast",
    "FirstOrder.Language.Ultraproduct.term_realize_cast",
    "FirstOrder.Language.Ultraproduct.boundedFormula_realize_cast",
    "FirstOrder.Language.Ultraproduct.realize_formula_cast",
    "FirstOrder.Language.Ultraproduct.sentence_realize",
    "Stage1Instances.THM_M_0673_Proof.boundedFormulaRealize_pinned",
    "Stage1Instances.THM_M_0673_Proof.formulaRealize_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.sentenceRealize_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.terminalRoot_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.losSentence_via_frozen",
    "Stage1Instances.THM_M_0673_Proof.losSentence_pinned",
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
assert output.count("Declarations are sorry-free!") >= 1
assert "sorryAx" not in output
assert "PROOF_CLOSURE bodyless_nonaxioms=[]" in output
assert "PROOF_CLOSURE unsafe=[]" in output
print("PASS THM-M-0673 proof Lean replay: exact pinned root and frozen composition")
PY
