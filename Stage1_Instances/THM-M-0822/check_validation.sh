#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0822"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0822-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --clearenv --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv ELAN_TOOLCHAIN leanprover/lean4:v4.29.0
  --setenv HOME "$tmp"
  --setenv PATH /usr/bin:/bin
  --setenv LEAN_NUM_THREADS 1
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv NO_COLOR 1 --setenv TZ UTC
  --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -j 1 -o Statement.olean Statement.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -j 1 -o ObligationTree.olean ObligationTree.lean \
  > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -j 1 -o Proof.olean Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -j 1 Validation.lean > "$tmp/validation.out"
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
    "Stage1Instances.THM_M_0822.ObligationTree.starConstruction_of_groundElement",
    "Stage1Instances.THM_M_0822.ObligationTree.starCard_of_image",
    "Stage1Instances.THM_M_0822.ObligationTree.attainment_of_starPackages",
    "Stage1Instances.THM_M_0822.ObligationTree.upperBound_of_mathlibTerminal",
    "Stage1Instances.THM_M_0822.ObligationTree.composeRoot",
    "Stage1Instances.THM_M_0822.ObligationTree.rootOfExactAssembly",
)
proof_declarations = (
    "Finset.erdos_ko_rado",
    "Stage1Instances.THM_M_0822.Proof.groundElement",
    "Stage1Instances.THM_M_0822.Proof.starConstruction",
    "Stage1Instances.THM_M_0822.Proof.starImage",
    "Stage1Instances.THM_M_0822.Proof.starIntersecting",
    "Stage1Instances.THM_M_0822.Proof.starSized",
    "Stage1Instances.THM_M_0822.Proof.starCard",
    "Stage1Instances.THM_M_0822.Proof.starAttainment",
    "Stage1Instances.THM_M_0822.Proof.mathlibUpperBound",
    "Stage1Instances.THM_M_0822.Proof.universalUpperBound",
    "Stage1Instances.THM_M_0822.Proof.exactAssembly",
    "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum",
)
validation_declarations = (
    "Finset.erdos_ko_rado",
    "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for declaration in composition_declarations:
    observed = observed_axioms(obligation_output, declaration)
    assert observed <= allowed and observed, declaration
for declaration in proof_declarations:
    observed = observed_axioms(proof_output, declaration)
    assert observed <= allowed and observed, declaration
for declaration in validation_declarations:
    assert observed_axioms(validation_output, declaration) == allowed, declaration
assert proof_output.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation_output.count("Declarations are sorry-free!") == len(validation_declarations)
assert (
    "Stage1Instances.THM_M_0822.Proof.erdosKoRadoMaximum : "
    "ErdosKoRadoMaximumTarget"
) in proof_output
combined = obligation_output + proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
