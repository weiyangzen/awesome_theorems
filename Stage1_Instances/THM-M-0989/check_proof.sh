#!/usr/bin/env bash
set -euo pipefail

repo_root="${STAGE1_REPO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
target="$repo_root/Stage1_Instances/THM-M-0989"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0989-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

tmp_target="$tmp/Stage1_Instances/THM-M-0989"
mkdir -p "$tmp_target"
cp "$target"/{Statement,ObligationTree,Proof,ProdExp,CharFunBound,LindebergArray}.lean \
  "$tmp_target/"

lean="$(cd "$lean_root" && lake env which lean)"
base_lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
lean_path="$tmp:$base_lean_path"

run_lean() {
  local source="$1"
  local output="$2"
  local log="$3"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
    "$lean" --trust=0 -o "$output" "$source" 2>&1 | tee "$log"
}

cd "$tmp_target"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" \
  "$lean" --trust=0 -o Statement.olean Statement.lean 2>&1 | tee Statement.out
run_lean ObligationTree.lean ObligationTree.olean ObligationTree.out
run_lean Proof.lean Proof.olean Proof.out
run_lean ProdExp.lean ProdExp.olean ProdExp.out
run_lean CharFunBound.lean CharFunBound.olean CharFunBound.out
run_lean LindebergArray.lean LindebergArray.olean LindebergArray.out

python3 - "$tmp_target" <<'PY'
import re
import sys
from pathlib import Path

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
        "Stage1Instances.THM_M_0989.ProductLimit.tendsto_row_prod_one_add_of_sum_norm_sq",
    ),
    "CharFunBound.out": (
        "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_sub_taylor_two_le",
        "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_one_sub_le_sq",
        "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_taylor_two_le",
        "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_taylor_two_le_crude",
        "Stage1Instances.THM_M_0989.CharFunBound.norm_cexp_mul_I_sub_one_sub_le_half_sq",
    ),
    "LindebergArray.out": (
        "Stage1Instances.THM_M_0989.rowSecondMoment_mem_unitInterval",
        "Stage1Instances.THM_M_0989.secondMoment_le_sq_add_truncated",
        "Stage1Instances.THM_M_0989.tendsto_sum_rowSecondMoment_sq",
        "Stage1Instances.THM_M_0989.rowLawCharFunConverges_proof",
        "Stage1Instances.THM_M_0989.lindebergFeller_exact",
    ),
}

for log_name, declarations in reports.items():
    output = (target / log_name).read_text(encoding="utf-8")
    if "error:" in output or "sorryAx" in output:
        raise SystemExit(f"invalid Lean output in {log_name}")
    for declaration in declarations:
        match = re.search(
            re.escape(f"'{declaration}' depends on axioms:")
            + r"\s*\[(.*?)\]",
            output,
            flags=re.DOTALL,
        )
        if match is None:
            raise SystemExit(f"missing axiom report for {declaration}")
        actual = {
            name.strip()
            for name in match.group(1).split(",")
            if name.strip()
        }
        if actual != allowed:
            raise SystemExit(f"unexpected axioms for {declaration}: {sorted(actual)}")

print(
    "PASS THM-M-0989 Lean proof: six modules elaborated with --trust=0; "
    "20 declarations have the allowed axiom set"
)
PY

printf '%s\n' \
  'statement_exit=0 obligation_tree_exit=0 proof_exit=0 prod_exp_exit=0 char_fun_bound_exit=0 lindeberg_array_exit=0'
