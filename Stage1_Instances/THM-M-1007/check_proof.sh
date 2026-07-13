#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1007"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-1007-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

export LEAN_NUM_THREADS=1
base_lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
cp "$target/Statement.lean" "$target/ObligationTree.lean" "$target/Proof.lean" "$tmp/"

cd "$lean_root"
lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$base_lean_path" lake env lean --trust=0 -t0 \
  --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" >/dev/null
LEAN_PATH="$tmp:$base_lean_path" lake env lean --trust=0 -t0 \
  --root="$tmp" "$tmp/Proof.lean" | tee "$tmp/proof.out"

if rg -n \
  '\b(sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|^[[:space:]]*(axiom|constant|opaque|unsafe)[[:space:]]+|\bextern[[:space:]]+' \
  "$target"/*.lean; then
  echo "forbidden Lean construct found" >&2
  exit 1
fi

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "measurable_truncationFunction",
    "measurable_truncate",
    "norm_truncate_le",
    "memLp_truncate",
    "integrable_truncate",
    "measurableSet_largeJump",
    "iIndepSet_largeJump",
    "iIndepFun_truncate",
    "largeJump_tsum_ne_top",
    "ae_eventually_no_largeJump",
    "summable_largeJump_of_ae_eventually_no_largeJump",
    "ae_eventually_no_largeJump_of_seriesConverges",
    "summable_largeJump_of_seriesConverges",
    "eventuallyEq_truncate",
    "seriesConverges_iff_of_eventuallyEq",
    "ae_seriesConverges_truncate_iff_of_summable_largeJump",
    "truncate_eq_centeredTruncate_add_mean",
    "measurable_centeredTruncationFunction",
    "measurable_centeredTruncate",
    "iIndepFun_centeredTruncate",
    "integral_centeredTruncate",
    "norm_centeredTruncate_le",
    "memLp_centeredTruncate",
    "variance_centeredTruncate",
    "seriesConverges_add_iff",
    "seriesConverges_centered_iff",
    "eLpNorm_one_le_two",
    "eLpNorm_one_le_sqrt_integral_sq",
    "ae_tendsto_sum_of_indep_centered_L1bdd",
    "ae_seriesConverges_centered_of_variance_summable",
    "ae_seriesConverges_truncate_of_mean_variance",
    "threeSeries_sufficiency",
    "obligationTree_sufficiency",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
prefix = "Stage1Instances.THM_M_1007.Proof."
for declaration in declarations:
    match = re.search(
        re.escape(f"'{prefix}{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        flags=re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert actual == allowed, (declaration, actual)
assert "sorryAx" not in output and "error:" not in output
print(f"PASS THM-M-1007 Lean proof: {len(declarations)} selected declarations")
print("all axiom reports exactly propext, Classical.choice, Quot.sound")
PY
