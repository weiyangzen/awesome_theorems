#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1005"
lean_root="$repo_root/Formalizations/Lean"
lean_cache="$lean_root/.lake"
tmp="$(mktemp -d "$lean_root/.m1005-validation.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,ObligationTree,DoobLp,Proof,Validation}.lean "$tmp/"

lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_cache="$(realpath "$lean_cache")"
lean_path="$lean_cache/build/lib/lean:$lean_cache/packages/mathlib/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/batteries/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/Qq/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/aesop/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/proofwidgets/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/importGraph/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/LeanSearchClient/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/plausible/.lake/build/lib/lean"
test -x "$lean_bin"
test -f "$lean_cache/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/Martingale/OptionalStopping.olean"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --chdir "$tmp"
)

"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" -t 0 -o Statement.olean Statement.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 -o DoobLp.olean DoobLp.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" -t 0 Validation.lean > "$tmp/validation.out"

python3 - "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

obligation_output = Path(sys.argv[1]).read_text(encoding="utf-8")
proof_output = Path(sys.argv[2]).read_text(encoding="utf-8")
validation_output = Path(sys.argv[3]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}


def observed_axioms(output: str, declaration: str) -> set[str]:
    if f"'{declaration}' does not depend on any axioms" in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


assert observed_axioms(
    obligation_output,
    "Stage1Instances.THM_M_1005.ObligationTree.root_of_strongDoobTerminal",
) <= allowed

proof_declarations = (
    "Stage1Instances.THM_M_1005.Proof.absSubmartingale",
    "Stage1Instances.THM_M_1005.Proof.measurable_runningAbsMax",
    "Stage1Instances.THM_M_1005.Proof.weakMaximal_abs",
    "MeasureTheory.maximal_ineq_Lp",
    "Stage1Instances.THM_M_1005.Proof.doobLpMomentEstimate",
    "Stage1Instances.THM_M_1005.Proof.doobLpMomentEstimate_via_frozen_composition",
)
for declaration in proof_declarations:
    assert observed_axioms(proof_output, declaration) == allowed, declaration

for declaration in (
    "MeasureTheory.maximal_ineq_Lp",
    "Stage1Instances.THM_M_1005.Validation.independentlyReconstructedDoobLpMomentEstimate",
):
    assert observed_axioms(validation_output, declaration) == allowed, declaration

assert validation_output.count("Declarations are sorry-free!") == 2
combined = obligation_output + proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined

print("PASS THM-M-1005 network-isolated narrow kernel replay")
print("PASS exact proof and differential roots: propext, Classical.choice, Quot.sound")
print("PASS transitive sorry check: vendored terminal and differential root are sorry-free")
PY
