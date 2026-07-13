#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1522"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1522-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,MaximalErgodic,Birkhoff,ObligationTree,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -o Statement.olean Statement.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -o MaximalErgodic.olean MaximalErgodic.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o Birkhoff.olean Birkhoff.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 Validation.lean > "$tmp/validation.out"
cat "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

obligation = Path(sys.argv[1]).read_text(encoding="utf-8")
proof = Path(sys.argv[2]).read_text(encoding="utf-8")
validation = Path(sys.argv[3]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
obligation_declarations = (
    "Stage1Instances.THM_M_1522.root_of_pointwise_and_identification",
)
proof_declarations = (
    "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
    "ErgodicTheory.tendsto_birkhoffAverage_ae",
    "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
    "Stage1Instances.THM_M_1522.generalPointwiseLimitPackage",
    "Stage1Instances.THM_M_1522.ergodicInvariantLimitIdentification",
    "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicViaFrozenComposition",
    "Stage1Instances.THM_M_1522.birkhoffPointwiseErgodicDirect",
)
validation_declarations = (
    "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
    "ErgodicTheory.tendsto_birkhoffAverage_ae",
    "ErgodicTheory.tendsto_birkhoffAverage_ae_integral",
    "Stage1Instances.THM_M_1522.Validation."
    "independentlyReconstructedBirkhoffPointwiseErgodic",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for output, declarations in (
    (obligation, obligation_declarations),
    (proof, proof_declarations),
    (validation, validation_declarations),
):
    for declaration in declarations:
        assert observed_axioms(output, declaration) == allowed, declaration

assert proof.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation.count("Declarations are sorry-free!") == len(validation_declarations)
combined = obligation + proof + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
