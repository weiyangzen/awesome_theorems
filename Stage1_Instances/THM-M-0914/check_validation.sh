#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0914"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0914-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
lean="$(cd "$lean_root" && lake env which lean)"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Fintype/Pigeonhole.olean"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Fintype/Card.olean"

base=(
  bwrap --clearenv --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv ELAN_TOOLCHAIN leanprover/lean4:v4.29.0
  --setenv HOME "$tmp"
  --setenv PATH /usr/bin:/bin
  --setenv LANG C --setenv LC_ALL C --setenv NO_COLOR 1 --setenv TZ UTC
  --chdir "$tmp"
)

"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean" --trust=0 -o Statement.olean Statement.lean >/dev/null 2>&1
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean" --trust=0 -o ObligationTree.olean ObligationTree.lean >/dev/null 2>&1
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean" --trust=0 Proof.lean >"$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean" --trust=0 Validation.lean >"$tmp/validation.out"

python3 - "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

proof = Path(sys.argv[1]).read_text(encoding="utf-8")
validation = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}

proof_namespace = "Stage1Instances.THM_M_0914.Proof."
proof_declarations = (
    "Finset.card_le_card_of_injOn",
    "Finset.exists_ne_map_eq_of_card_lt_of_maps_to",
    "Fintype.exists_ne_map_eq_of_card_lt",
    proof_namespace + "cardInjOnBound_pinned",
    proof_namespace + "finsetCollision_pinned",
    proof_namespace + "finsetCollision_from_frozen_children",
    proof_namespace + "fintypeWrapper_pinned",
    proof_namespace + "fintypeWrapper_from_frozen_children",
    proof_namespace + "root_via_pinned_wrapper",
    proof_namespace + "root_via_frozen_children",
    proof_namespace + "pigeonholeTarget_proof",
    proof_namespace + "pigeonholeTarget_via_frozen_children",
)
validation_declarations = (
    "Fintype.not_injective_of_card_lt",
    "Function.not_injective_iff",
    "Stage1Instances.THM_M_0914.Validation.pigeonholeTarget_differential",
)

def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}

for declaration in proof_declarations:
    assert observed_axioms(proof, declaration) == allowed, declaration
for declaration in validation_declarations:
    assert observed_axioms(validation, declaration) == allowed, declaration
assert proof.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation.count("Declarations are sorry-free!") == len(validation_declarations)
assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation
assert "VALIDATION_CLOSURE unsafe=[]" in validation
assert "sorryAx" not in proof + validation
assert "error:" not in proof + validation
print(
    "PASS THM-M-0914 network-isolated validation: exact proof and differential "
    "roots replayed; 15 declarations sorry-free; axioms within "
    "propext, Classical.choice, Quot.sound; closure has no unsafe or bodyless nonaxioms"
)
PY
