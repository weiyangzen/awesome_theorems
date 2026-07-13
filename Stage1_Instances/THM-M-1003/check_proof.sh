#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1003"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1003-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"

cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean_bin" -o Statement.olean Statement.lean >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" \
  "$lean_bin" -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" \
  "$lean_bin" Proof.lean | tee proof.out

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1003.Proof.convexOn_univ_norm_rpow",
    "Stage1Instances.THM_M_1003.Proof.continuous_norm_rpow",
    "Stage1Instances.THM_M_1003.Proof.eLpNorm_condExp_le",
    "Stage1Instances.THM_M_1003.Proof.boundedCondExpTendstoLp",
    "Stage1Instances.THM_M_1003.Proof.unifIntegrableOfAeBound",
    "Stage1Instances.THM_M_1003.Proof.memLpTendstoCondExp",
    "Stage1Instances.THM_M_1003.Proof.uniformL1Bound",
    "Stage1Instances.THM_M_1003.Proof.limitCandidate",
    "Stage1Instances.THM_M_1003.Proof.candidatePackage",
    "Stage1Instances.THM_M_1003.Proof.uniformL1UI",
    "Stage1Instances.THM_M_1003.Proof.sameExponentNormCanonical",
    "Stage1Instances.THM_M_1003.Proof.sameExponentPackage",
    "Stage1Instances.THM_M_1003.Proof.target",
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

assert output.count("Declarations are sorry-free!") == len(declarations)
assert "Stage1Instances.THM_M_1003.Proof.target.{u} : LpMartingaleConvergenceTarget" in output
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
PY
