#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0990"
dependency="$repo_root/Stage1_Instances/THM-M-0989"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0990-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/Stage1_Instances/THM-M-0990" "$tmp/Stage1_Instances/THM-M-0989"
cp "$target"/{Statement,Normalization,ProductLimit,GeneralizedLindeberg,Proof,Validation}.lean \
  "$tmp/Stage1_Instances/THM-M-0990/"
cp "$dependency"/{Statement,ObligationTree,Proof,CharFunBound}.lean \
  "$tmp/Stage1_Instances/THM-M-0989/"

lean="$(cd "$lean_root" && lake env which lean)"
base_lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
lean_path="$tmp:$base_lean_path"
tmp="$(realpath "$tmp")"

base=(
  bwrap --clearenv --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv ELAN_TOOLCHAIN leanprover/lean4:v4.29.0
  --setenv HOME "$tmp" --setenv PATH /usr/bin:/bin
  --setenv LANG C --setenv LC_ALL C --setenv NO_COLOR 1 --setenv TZ UTC
)

run_module() {
  local source="$1"
  local output="$2"
  local log="$3"
  local module_path="$4"
  "${base[@]}" --chdir "$(dirname "$source")" --setenv LEAN_PATH "$module_path" \
    "$lean" --trust=0 --root "$tmp" -o "$output" "$source" >"$log"
}

dependency_dir="$tmp/Stage1_Instances/THM-M-0989"
target_dir="$tmp/Stage1_Instances/THM-M-0990"

run_module "$dependency_dir/Statement.lean" "$dependency_dir/Statement.olean" \
  "$dependency_dir/Statement.out" "$base_lean_path"
run_module "$dependency_dir/ObligationTree.lean" "$dependency_dir/ObligationTree.olean" \
  "$dependency_dir/ObligationTree.out" "$lean_path"
run_module "$dependency_dir/Proof.lean" "$dependency_dir/Proof.olean" \
  "$dependency_dir/Proof.out" "$lean_path"
run_module "$dependency_dir/CharFunBound.lean" "$dependency_dir/CharFunBound.olean" \
  "$dependency_dir/CharFunBound.out" "$lean_path"

run_module "$target_dir/Statement.lean" "$target_dir/Statement.olean" \
  "$target_dir/Statement.out" "$base_lean_path"
run_module "$target_dir/Normalization.lean" "$target_dir/Normalization.olean" \
  "$target_dir/Normalization.out" "$lean_path"
run_module "$target_dir/ProductLimit.lean" "$target_dir/ProductLimit.olean" \
  "$target_dir/ProductLimit.out" "$lean_path"
run_module "$target_dir/GeneralizedLindeberg.lean" "$target_dir/GeneralizedLindeberg.olean" \
  "$target_dir/GeneralizedLindeberg.out" "$lean_path"
run_module "$target_dir/Proof.lean" "$target_dir/Proof.olean" \
  "$target_dir/Proof.out" "$lean_path"
run_module "$target_dir/Validation.lean" "$target_dir/Validation.olean" \
  "$target_dir/Validation.out" "$lean_path"

cat "$target_dir"/{Normalization,ProductLimit,GeneralizedLindeberg,Proof,Validation}.out

python3 -I - "$target_dir" <<'PY'
import re
import sys
from pathlib import Path

if not __debug__:
    raise RuntimeError("validation requires Python assertions (__debug__ must be true)")

target = Path(sys.argv[1])
allowed = {"propext", "Classical.choice", "Quot.sound"}
reports = {
    "Normalization.out": (
        "Stage1Instances.THM_M_0990.centered_measurable",
        "Stage1Instances.THM_M_0990.centered_memLp",
        "Stage1Instances.THM_M_0990.centered_integral_eq_zero",
        "Stage1Instances.THM_M_0990.normalizedIncrement_memLp",
        "Stage1Instances.THM_M_0990.normalizedIncrement_integral_eq_zero",
        "Stage1Instances.THM_M_0990.normalizedIncrement_independent",
        "Stage1Instances.THM_M_0990.normalizedIncrement_variance_sum",
        "Stage1Instances.THM_M_0990.normalizedIncrement_sum",
    ),
    "ProductLimit.out": (
        "Stage1Instances.THM_M_0990.ProductLimit."
        "tendsto_row_prod_one_add_of_sum_norm_sq",
    ),
    "GeneralizedLindeberg.out": (
        "Stage1Instances.THM_M_0990.eventualRowSumsAEMeasurable_proof",
        "Stage1Instances.THM_M_0990.eventualRowCharFun_factorization",
        "Stage1Instances.THM_M_0990.eventually_rowSecondMoment_sum",
        "Stage1Instances.THM_M_0990.eventually_rowGaussianQuadraticCoefficient",
        "Stage1Instances.THM_M_0990.eventual_root_of_row_charFun_packages",
        "Stage1Instances.THM_M_0990.rowSecondMoment_mem_unitInterval",
        "Stage1Instances.THM_M_0990.secondMoment_le_sq_add_truncated",
        "Stage1Instances.THM_M_0990.tendsto_sum_rowSecondMoment_sq",
        "Stage1Instances.THM_M_0990.eventualRowLawCharFunConverges_proof",
        "Stage1Instances.THM_M_0990.eventualLindebergFeller_exact",
    ),
    "Proof.out": (
        "Stage1Instances.THM_M_0990.sq_le_rpow_mul_final",
        "Stage1Instances.THM_M_0990.truncatedSecondMoment_scaled_le_final",
        "Stage1Instances.THM_M_0990.sum_truncatedSecondMoment_normalized_le_final",
        "Stage1Instances.THM_M_0990.normalizedRowSum_measurable_final",
        "Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact",
    ),
    "Validation.out": (
        "Stage1Instances.THM_M_0990.lyapunovCentralLimit_exact",
        "Stage1Instances.THM_M_0990.Validation."
        "lyapunovCentralLimit_composition_replay",
        "Stage1Instances.THM_M_0990.eventualLindebergFeller_exact",
        "MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun",
        "ProbabilityTheory.iIndepFun.charFun_map_fun_sum_eq_prod",
        "ProbabilityTheory.charFun_gaussianReal",
    ),
}


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[(.*?)]",
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
assert validation.count("Declarations are sorry-free!") == 6
closure_match = re.search(
    r"VALIDATION_CLOSURE declarations=(\d+) modules=(\d+)", validation
)
assert closure_match is not None
assert int(closure_match.group(1)) > 50000
assert int(closure_match.group(2)) > 1500
assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation
assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation
assert "VALIDATION_CLOSURE unsafe=[]" in validation
combined = "".join((target / name).read_text(encoding="utf-8") for name in reports)
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
print(
    "PASS THM-M-0990 network-isolated validation: exact root and separate "
    "composition replayed; 30 axiom reports passed; transitive closure has "
    "no unsafe or unexpected bodyless declarations"
)
PY
