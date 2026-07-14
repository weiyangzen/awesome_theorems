#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1084"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1084-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"

cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean_bin" --trust=0 -o "$tmp/Statement.olean" Statement.lean >"$tmp/statement.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean_bin" --trust=0 GaussianMGFBridge.lean >"$tmp/mgf.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean_bin" --trust=0 CoveringNets.lean >"$tmp/nets.out" 2>&1

python3 - "$tmp/mgf.out" "$tmp/nets.out" <<'PY'
import re
import sys
from pathlib import Path

output = "\n".join(Path(path).read_text(encoding="utf-8") for path in sys.argv[1:])
declarations = (
    "hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero",
    "increment_mgf_eq_dist_sq",
    "increment_hasSubgaussianMGF",
    "gaussianIncrementMGFPackage",
    "exists_openBallCover",
    "exists_minimal_openBallCover",
    "coveringNumber_pos",
)
namespace = "Stage1Instances.THM_M_1084.Proof."
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

printf '%s\n' \
  "PASS THM-M-1084 partial proof: exact Gaussian-MGF and finite-net bodies elaborate with --trust=0" \
  "axioms are limited to propext, Classical.choice, and Quot.sound; root remains open"
