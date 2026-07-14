#!/usr/bin/env bash
set -euo pipefail

if (( $# != 0 )); then
  printf 'usage: %s\n' "$0" >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1119"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1119-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"
lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 540 "$lean_bin" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" \
  timeout 540 "$lean_bin" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" \
  timeout 540 "$lean_bin" --trust=0 -t0 Proof.lean > proof.out
cat proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1119.openGraph_adj_of_open",
    "Stage1Instances.THM_M_1119.openGraph_mono",
    "Stage1Instances.THM_M_1119.originInInfiniteCluster_mono",
    "Stage1Instances.THM_M_1119.openGraph_reachable_of_walk",
    "Stage1Instances.THM_M_1119.measurable_openGraph_reachable",
    "Stage1Instances.THM_M_1119.measurable_originInInfiniteCluster",
    "Stage1Instances.THM_M_1119.bondMeasure_one_eq_dirac",
    "Stage1Instances.THM_M_1119.originInInfiniteCluster_allOpen",
    "Stage1Instances.THM_M_1119.one_mem_positiveParameters",
    "Stage1Instances.THM_M_1119.criticalProbability_le_one",
    "Stage1Instances.THM_M_1119.bondMeasure_zero_eq_dirac",
    "Stage1Instances.THM_M_1119.percolationProbability_zero",
    "Stage1Instances.THM_M_1119.zero_not_mem_positiveParameters",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-1119 isolated Lean replay: graph, measurability, and endpoint bodies checked")
PY
