#!/usr/bin/env bash
set -euo pipefail

repo_root="${STAGE1_REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
target="$repo_root/Stage1_Instances/THM-M-0990"
dependency="$repo_root/Stage1_Instances/THM-M-0989"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0990-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/Stage1_Instances/THM-M-0990" "$tmp/Stage1_Instances/THM-M-0989"
cp "$target"/{Statement,Normalization,ProductLimit,GeneralizedLindeberg,Proof}.lean \
  "$tmp/Stage1_Instances/THM-M-0990/"
cp "$dependency"/{Statement,ObligationTree,Proof,CharFunBound}.lean \
  "$tmp/Stage1_Instances/THM-M-0989/"

base_lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
lean_path="$tmp:$base_lean_path"

run_lean() {
  local source="$PWD/$1"
  local output="$PWD/$2"
  local log="$PWD/$3"
  (cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
    lake env lean --trust=0 --root "$tmp" -o "$output" "$source") 2>&1 | tee "$log"
}

run_base_lean() {
  local source="$PWD/$1"
  local output="$PWD/$2"
  local log="$PWD/$3"
  (cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" \
    lake env lean --trust=0 --root "$tmp" -o "$output" "$source") 2>&1 | tee "$log"
}

cd "$tmp/Stage1_Instances/THM-M-0989"
run_base_lean Statement.lean Statement.olean Statement.out
run_lean ObligationTree.lean ObligationTree.olean ObligationTree.out
run_lean Proof.lean Proof.olean Proof.out
run_lean CharFunBound.lean CharFunBound.olean CharFunBound.out

cd "$tmp/Stage1_Instances/THM-M-0990"
run_base_lean Statement.lean Statement.olean Statement.out
run_lean Normalization.lean Normalization.olean Normalization.out
run_lean ProductLimit.lean ProductLimit.olean ProductLimit.out
run_lean GeneralizedLindeberg.lean GeneralizedLindeberg.olean GeneralizedLindeberg.out
run_lean Proof.lean Proof.olean Proof.out

python3 - "$tmp/Stage1_Instances/THM-M-0990" <<'PY'
import re
import sys
from pathlib import Path

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
        "Stage1Instances.THM_M_0990.ProductLimit.tendsto_row_prod_one_add_of_sum_norm_sq",
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
}

for log_name, declarations in reports.items():
    output = (target / log_name).read_text(encoding="utf-8")
    if "error:" in output or "sorryAx" in output:
        raise SystemExit(f"invalid Lean output in {log_name}")
    for declaration in declarations:
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms:") + r"\s*\[(.*?)\]",
            output,
            flags=re.DOTALL,
        )
        if match is None:
            raise SystemExit(f"missing axiom report for {declaration}")
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        if actual != allowed:
            raise SystemExit(f"unexpected axioms for {declaration}: {sorted(actual)}")

source_probe_count = 0
for source_name in ("Normalization.lean", "ProductLimit.lean", "GeneralizedLindeberg.lean", "Proof.lean"):
    source_probe_count += (target / source_name).read_text(encoding="utf-8").count("#print axioms")
expected_probe_count = sum(len(declarations) for declarations in reports.values())
if source_probe_count != expected_probe_count or expected_probe_count != 24:
    raise SystemExit(
        f"axiom-probe inventory mismatch: source={source_probe_count}, expected={expected_probe_count}"
    )

print(
    "PASS THM-M-0990 Lean proof: nine isolated modules elaborated with --trust=0; "
    "24 target declarations have the allowed axiom set"
)
PY

printf '%s\n' \
  'dependency_exit=0 statement_exit=0 normalization_exit=0 product_limit_exit=0 generalized_lindeberg_exit=0 proof_exit=0'
