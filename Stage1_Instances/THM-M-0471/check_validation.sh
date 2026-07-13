#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0471"
lean_cache="$repo_root/Formalizations/Lean/.lake"
tmp="$(mktemp -d /tmp/stage1-m0471-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lake_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
lean_path="$lean_cache/build/lib/lean:$lean_cache/packages/mathlib/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/batteries/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/Qq/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/aesop/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/proofwidgets/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/importGraph/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/LeanSearchClient/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/plausible/.lake/build/lib/lean"
test -x "$lean_bin"
test -x "$lake_bin"
test -f "$lean_cache/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Nat/Factors.olean"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lake_bin" env lean -t 0 -o Statement.olean Statement.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lake_bin" env lean -t 0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lake_bin" env lean -t 0 Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lake_bin" env lean -t 0 Validation.lean > "$tmp/validation.out"
cat "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

obligation_output = Path(sys.argv[1]).read_text(encoding="utf-8")
proof_output = Path(sys.argv[2]).read_text(encoding="utf-8")
validation_output = Path(sys.argv[3]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
composition_declarations = (
    "Stage1Instances.THM_M_0471.ObligationTree.exactPrimeListAnchor_of_packages",
    "Stage1Instances.THM_M_0471.ObligationTree.root_of_exactPrimeListAnchor",
)
proof_declarations = (
    "Nat.primeFactorsList_ne_nil",
    "Nat.prime_of_mem_primeFactorsList",
    "Nat.prod_primeFactorsList",
    "Nat.primeFactorsList_unique",
    "perm_of_prod_eq_prod",
    "Prime.dvd_prod_iff",
    "mem_list_primes_of_dvd_prod",
    "List.perm_cons_erase",
    "mul_right_inj'",
    "Stage1Instances.THM_M_0471.Proof.nonzeroNormalization",
    "Stage1Instances.THM_M_0471.Proof.primeDvdProduct",
    "Stage1Instances.THM_M_0471.Proof.primeDivisorMembership",
    "Stage1Instances.THM_M_0471.Proof.erasePermutation",
    "Stage1Instances.THM_M_0471.Proof.cancelCommonHead",
    "Stage1Instances.THM_M_0471.Proof.primeProductPermutation",
    "Stage1Instances.THM_M_0471.Proof.witnessNonempty",
    "Stage1Instances.THM_M_0471.Proof.witnessPrimality",
    "Stage1Instances.THM_M_0471.Proof.witnessProduct",
    "Stage1Instances.THM_M_0471.Proof.primeFactorUniqueness",
    "Stage1Instances.THM_M_0471.Proof.primeFactorUniqueness_via_components",
    "Stage1Instances.THM_M_0471.Proof.exactPrimeListAnchor",
    "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic_via_frozen_composition",
    "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic",
)
validation_declarations = (
    "Nat.primeFactorsList_ne_nil",
    "Nat.prime_of_mem_primeFactorsList",
    "Nat.prod_primeFactorsList",
    "Nat.primeFactorsList_unique",
    "Stage1Instances.THM_M_0471.Validation."
    "independentlyReconstructedFundamentalTheoremOfArithmetic",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    if no_axioms in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for declaration in composition_declarations:
    assert observed_axioms(obligation_output, declaration) <= allowed, declaration
for declaration in proof_declarations:
    assert observed_axioms(proof_output, declaration) <= allowed, declaration
for declaration in validation_declarations:
    assert observed_axioms(validation_output, declaration) <= allowed, declaration
for output, declaration in (
    (proof_output, "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic"),
    (proof_output, "Stage1Instances.THM_M_0471.Proof.fundamentalTheoremOfArithmetic_via_frozen_composition"),
    (validation_output, "Stage1Instances.THM_M_0471.Validation."
        "independentlyReconstructedFundamentalTheoremOfArithmetic"),
):
    assert observed_axioms(output, declaration) == allowed, declaration
assert proof_output.count("Declarations are sorry-free!") == 24
assert validation_output.count("Declarations are sorry-free!") == 1
combined = obligation_output + proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
