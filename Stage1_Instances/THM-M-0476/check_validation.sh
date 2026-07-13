#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0476"
lean_cache="$repo_root/Formalizations/Lean/.lake"
tmp="$(mktemp -d /tmp/stage1-m0476-validation.XXXXXX)"
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
test -f "$lean_cache/packages/mathlib/.lake/build/lib/lean/Mathlib/NumberTheory/Wilson.olean"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lake_bin" env lean -t 0 -o Statement.olean Statement.lean > "$tmp/statement.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lake_bin" env lean -t 0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lake_bin" env lean -t 0 Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lake_bin" env lean -t 0 Validation.lean > "$tmp/validation.out"

cat "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
  "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

statement_output = Path(sys.argv[1]).read_text(encoding="utf-8")
obligation_output = Path(sys.argv[2]).read_text(encoding="utf-8")
proof_output = Path(sys.argv[3]).read_text(encoding="utf-8")
validation_output = Path(sys.argv[4]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}

statement_declarations = (
    "Stage1Instances.THM_M_0476.wilsonTheoremTarget_iff_factTarget",
    "Stage1Instances.THM_M_0476.mutationIncludedCompositeFour_false",
)
obligation_declarations = (
    "Stage1Instances.THM_M_0476.ObligationTree.factorialProduct_of_identities",
    "Stage1Instances.THM_M_0476.ObligationTree.residueUnitsProduct_of_components",
    "Stage1Instances.THM_M_0476.ObligationTree.unitEraseProduct_of_inversion",
    "Stage1Instances.THM_M_0476.ObligationTree.unitProductIdentity_of_erase",
    "Stage1Instances.THM_M_0476.ObligationTree.unitsProductBridge_of_components",
    "Stage1Instances.THM_M_0476.ObligationTree.factWilsonAnchor_of_bridges",
    "Stage1Instances.THM_M_0476.ObligationTree.root_of_factWilsonAnchor",
    "Stage1Instances.THM_M_0476.ObligationTree.root_of_composedTarget",
)
upstream = (
    "ZMod.wilsons_lemma",
    "FiniteField.prod_univ_units_id_eq_neg_one",
    "Finset.prod_Ico_id_eq_factorial",
    "Finset.prod_natCast",
)
proof_local = tuple(
    "Stage1Instances.THM_M_0476.Proof." + name
    for name in (
        "factWilsonAnchor_mathlib",
        "unitProductIdentity_mathlib",
        "factorialIntervalIdentity",
        "natIntervalCastIdentity",
        "primeEndpointIdentity",
        "unitRepresentativeInPrimeRange",
        "unitRepresentativeInjective",
        "residueRepresentativeSurjectiveAtEndpoint",
        "representativeCastAgreement",
        "inverseFixedPointClassification",
        "factorialProduct",
        "residueUnitsProduct",
        "unitEraseNegOneProduct",
        "unitProductIdentity_expanded",
        "unitsProductBridge",
        "factWilsonAnchor_expanded",
        "wilsonTheorem_after_factTransport",
        "wilsonTheorem_via_frozen_composition",
        "wilsonTheorem",
    )
)
validation_declarations = (
    "Nat.prime_iff_fac_equiv_neg_one",
    "Stage1Instances.THM_M_0476.Validation."
    "wilsonTheorem_via_primeCharacterization",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    if f"'{declaration}' does not depend on any axioms" in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for output, declarations in (
    (statement_output, statement_declarations),
    (obligation_output, obligation_declarations),
    (proof_output, upstream + proof_local),
    (validation_output, validation_declarations),
):
    for declaration in declarations:
        assert observed_axioms(output, declaration) <= allowed, declaration

for output, declaration in (
    (proof_output, "Stage1Instances.THM_M_0476.Proof.wilsonTheorem"),
    (proof_output, "Stage1Instances.THM_M_0476.Proof.wilsonTheorem_via_frozen_composition"),
    (validation_output, "Stage1Instances.THM_M_0476.Validation."
        "wilsonTheorem_via_primeCharacterization"),
):
    assert observed_axioms(output, declaration) == allowed, declaration

assert proof_output.count("Declarations are sorry-free!") == 23
assert validation_output.count("Declarations are sorry-free!") == 2
combined = statement_output + obligation_output + proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
