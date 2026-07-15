#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1085"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1085-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

mkdir -p "$tmp/Stage1_Instances/THM-M-1085"
cp "$target/Statement.lean" "$target/LawReduction.lean" "$tmp/Stage1_Instances/THM-M-1085/"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 600 \
  "$lean_bin" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Stage1_Instances/THM-M-1085/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1085/Statement.lean" >statement.out 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 600 \
  "$lean_bin" --trust=0 -t0 -R "$tmp" \
  "$tmp/Stage1_Instances/THM-M-1085/LawReduction.lean" >law-reduction.out 2>&1

if ! python3 - law-reduction.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "measurableSet_belowAllRange",
    "measurableSet_belowAllEuclidean",
    "coordinate_hasGaussianLaw",
    "coordinate_integrable",
    "isProbabilityMeasure_of_hasGaussianLaw",
    "pushforward_hasLaw",
    "map_apply_belowAllRange",
    "map_toLp_apply_belowAllEuclidean",
    "integral_coordinate_map",
    "covariance_coordinate_map",
    "covarianceMatrix_eq",
    "covarianceMatrix_posSemidef",
    "covarianceMatrix_diag_eq",
    "covarianceMatrix_offdiag_le",
    "covarianceMatrix_order_data",
    "integral_toLp_map_eq_zero",
    "covarianceBilin_map_eq_multivariateGaussian",
    "gaussian_law_eq_multivariateGaussian",
    "belowAll_eq_multivariateGaussian",
    "slepianTarget_of_law",
)
namespace = "Stage1Instances.THM_M_1085.Proof."
allowed = {"propext", "Classical.choice", "Quot.sound"}
for short_name in declarations:
    declaration = namespace + short_name
    no_axioms = f"'{declaration}' does not depend on any axioms"
    report = re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]"
    matches = re.findall(report, output, re.DOTALL)
    count = output.count(no_axioms) + len(matches)
    assert count == 1, f"expected one axiom report for {declaration}, got {count}"
    if matches:
        actual = {name.strip() for name in matches[0].split(",") if name.strip()}
        assert actual <= allowed, f"unexpected axioms for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
assert "error:" not in output
PY
then
  cat law-reduction.out >&2
  exit 1
fi

printf '%s\n' \
  "PASS THM-M-1085 partial proof: finite-law reduction bodies elaborate with --trust=0" \
  "twenty declarations are sorry-free; axioms are limited to propext, Classical.choice, and Quot.sound" \
  "the Gaussian-law orthant comparison and exact root remain open"

cd "$repo_root"
python3 "$target/check_statement.py"
python3 "$target/check_proof.py"
