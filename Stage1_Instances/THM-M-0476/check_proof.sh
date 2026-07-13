#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0476"
lean_cache="$repo_root/Formalizations/Lean/.lake"
tmp="$(mktemp -d /tmp/stage1-m0476-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_path="$lean_cache/build/lib/lean:$lean_cache/packages/mathlib/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/batteries/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/Qq/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/aesop/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/proofwidgets/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/importGraph/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/LeanSearchClient/.lake/build/lib/lean"
lean_path+=":$lean_cache/packages/plausible/.lake/build/lib/lean"

test -f "$lean_cache/packages/mathlib/.lake/build/lib/lean/Mathlib/NumberTheory/Wilson.olean"
cd "$repo_root/Formalizations/Lean"
LEAN_PATH="$lean_path" lake env lean --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$lean_path" lake env lean --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >/dev/null
LEAN_PATH="$tmp:$lean_path" lake env lean --root="$tmp" "$tmp/Proof.lean" | tee "$tmp/Proof.out"

python3 - "$tmp/Proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
namespace = "Stage1Instances.THM_M_0476.Proof."
upstream = (
    "ZMod.wilsons_lemma",
    "FiniteField.prod_univ_units_id_eq_neg_one",
    "Finset.prod_Ico_id_eq_factorial",
    "Finset.prod_natCast",
)
local = (
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
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in upstream + tuple(namespace + name for name in local):
    no_axioms = f"'{declaration}' does not depend on any axioms"
    if no_axioms in output:
        continue
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == 23
assert "sorryAx" not in output
assert "warning:" not in output
assert "error:" not in output
print("PASS THM-M-0476 Lean proof: 23 declarations sorry-free; axiom closure allowlisted")
PY
