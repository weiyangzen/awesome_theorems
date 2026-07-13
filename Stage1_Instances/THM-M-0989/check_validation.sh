#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0989"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0989-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof,ProdExp,CharFunBound,LindebergArray,Validation}.lean \
  "$tmp/"

lean="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --clearenv --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv ELAN_TOOLCHAIN leanprover/lean4:v4.29.0
  --setenv HOME "$tmp" --setenv PATH /usr/bin:/bin
  --setenv LANG C --setenv LC_ALL C --setenv NO_COLOR 1 --setenv TZ UTC
  --chdir "$tmp"
)

run_module() {
  local source="$1"
  local output="$2"
  local log="$3"
  "${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
    "$lean" --trust=0 -o "$output" "$source" >"$log"
}

"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean" --trust=0 -o Statement.olean Statement.lean >/dev/null
mkdir -p "$tmp/Stage1_Instances/THM-M-0989"
ln -s "$tmp/Statement.olean" "$tmp/Stage1_Instances/THM-M-0989/Statement.olean"
run_module ObligationTree.lean ObligationTree.olean "$tmp/ObligationTree.out"
ln -s "$tmp/ObligationTree.olean" "$tmp/Stage1_Instances/THM-M-0989/ObligationTree.olean"
run_module Proof.lean Proof.olean "$tmp/Proof.out"
ln -s "$tmp/Proof.olean" "$tmp/Stage1_Instances/THM-M-0989/Proof.olean"
run_module ProdExp.lean ProdExp.olean "$tmp/ProdExp.out"
ln -s "$tmp/ProdExp.olean" "$tmp/Stage1_Instances/THM-M-0989/ProdExp.olean"
run_module CharFunBound.lean CharFunBound.olean "$tmp/CharFunBound.out"
ln -s "$tmp/CharFunBound.olean" "$tmp/Stage1_Instances/THM-M-0989/CharFunBound.olean"
run_module LindebergArray.lean LindebergArray.olean "$tmp/LindebergArray.out"
ln -s "$tmp/LindebergArray.olean" "$tmp/Stage1_Instances/THM-M-0989/LindebergArray.olean"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean" --trust=0 Validation.lean >"$tmp/Validation.out"

cat "$tmp"/{Proof,ProdExp,CharFunBound,LindebergArray,Validation}.out

python3 -I - "$tmp" <<'PY'
import re
import sys
from pathlib import Path

if not __debug__:
    raise RuntimeError("validation requires Python assertions (__debug__ must be true)")

target = Path(sys.argv[1])
allowed = {"propext", "Classical.choice", "Quot.sound"}
reports = {
    "Proof.out": (
        "Stage1Instances.THM_M_0989.rowSumsAEMeasurable_proof",
        "Stage1Instances.THM_M_0989.rowCharFun_factorization",
        "Stage1Instances.THM_M_0989.rowSecondMoment_sum",
        "Stage1Instances.THM_M_0989.rowExpectation_sum",
        "Stage1Instances.THM_M_0989.rowGaussianQuadraticCoefficient",
        "Stage1Instances.THM_M_0989.truncatedSecondMoment_nonneg",
        "Stage1Instances.THM_M_0989.integrable_truncatedSecondMoment_integrand",
        "Stage1Instances.THM_M_0989.truncatedSecondMoment_le_secondMoment",
        "Stage1Instances.THM_M_0989.root_of_row_charFun_convergence",
    ),
    "ProdExp.out": (
        "Stage1Instances.THM_M_0989.ProductLimit."
        "tendsto_row_prod_one_add_of_sum_norm_sq",
    ),
    "CharFunBound.out": (
        "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_sub_taylor_two_le",
        "Stage1Instances.THM_M_0989.CharFunBound."
        "norm_cexp_mul_I_sub_one_sub_le_sq",
        "Stage1Instances.THM_M_0989.CharFunBound."
        "norm_cexp_mul_I_sub_taylor_two_le",
        "Stage1Instances.THM_M_0989.CharFunBound."
        "norm_cexp_mul_I_sub_taylor_two_le_crude",
        "Stage1Instances.THM_M_0989.CharFunBound."
        "norm_cexp_mul_I_sub_one_sub_le_half_sq",
    ),
    "LindebergArray.out": (
        "Stage1Instances.THM_M_0989.rowSecondMoment_mem_unitInterval",
        "Stage1Instances.THM_M_0989.secondMoment_le_sq_add_truncated",
        "Stage1Instances.THM_M_0989.tendsto_sum_rowSecondMoment_sq",
        "Stage1Instances.THM_M_0989.rowLawCharFunConverges_proof",
        "Stage1Instances.THM_M_0989.lindebergFeller_exact",
    ),
    "Validation.out": (
        "Stage1Instances.THM_M_0989.lindebergFeller_exact",
        "Stage1Instances.THM_M_0989.Validation.lindebergFeller_composition_replay",
        "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
        "ProbabilityTheory.iIndepFun.charFun_map_fun_sum_eq_prod",
        "ProbabilityTheory.charFun_gaussianReal",
    ),
}


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match is not None, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for log_name, declarations in reports.items():
    output = (target / log_name).read_text(encoding="utf-8")
    assert "error:" not in output, f"Lean error in {log_name}"
    for declaration in declarations:
        assert observed_axioms(output, declaration) == allowed, declaration

validation = (target / "Validation.out").read_text(encoding="utf-8")
assert validation.count("Declarations are sorry-free!") == 5
assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation
assert "VALIDATION_CLOSURE unsafe=[]" in validation
combined = "".join((target / name).read_text(encoding="utf-8") for name in reports)
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
print(
    "PASS THM-M-0989 network-isolated validation: exact root and final "
    "composition replayed; 25 axiom reports passed; validation closure has "
    "no unsafe or unexpected bodyless declarations"
)
PY
