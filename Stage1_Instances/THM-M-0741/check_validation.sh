#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0741"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0741-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --bind / / --dev /dev --proc /proc --unshare-net --die-with-parent
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" -t 0 -o Statement.olean Statement.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 -o ObligationTree.olean ObligationTree.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 Validation.lean > "$tmp/validation.out"
cat "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

proof_output = Path(sys.argv[1]).read_text(encoding="utf-8")
validation_output = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
proof_declarations = (
    "ComputablePred.rice",
    "ComputablePred.halting_problem",
    "Stage1Instances.THM_M_0741.Proof.riceBridge_pinned",
    "Stage1Instances.THM_M_0741.Proof.fixedInputZeroUndecidable_via_rice",
    "Stage1Instances.THM_M_0741.Proof.fixedInputZeroUndecidable_pinned",
    "Stage1Instances.THM_M_0741.Proof.fixedInputReduction_checked",
    "Stage1Instances.THM_M_0741.Proof.haltingProblemUndecidable",
    "Stage1Instances.THM_M_0741.Proof.haltingProblemUndecidable_via_rice",
)
validation_declarations = (
    "Stage1Instances.THM_M_0741.Validation."
    "independentlyReconstructedHaltingProblemUndecidable",
    "ComputablePred.halting_problem",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for declaration in proof_declarations:
    assert observed_axioms(proof_output, declaration) == allowed, declaration
for declaration in validation_declarations:
    assert observed_axioms(validation_output, declaration) == allowed, declaration
assert proof_output.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation_output.count("Declarations are sorry-free!") == len(validation_declarations)
combined = proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
