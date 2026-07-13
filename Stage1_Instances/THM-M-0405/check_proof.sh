#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0405"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0405-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"

cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean_bin" --trust=0 -o "$tmp/Statement.olean" Statement.lean >"$tmp/statement.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o "$tmp/ObligationTree.olean" ObligationTree.lean \
  >"$tmp/obligation-tree.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean_bin" --trust=0 Proof.lean >"$tmp/proof.out" 2>&1

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "ne_of_ratioNotRootOfUnity",
    "LucasPair.alpha_ne_zero",
    "LucasPair.beta_ne_zero",
    "LucasPair.alpha_ne_beta",
    "LucasPair.denominator_ne_zero",
    "LucasPair.coe_discriminant",
    "LucasPair.term_zero",
    "LucasPair.term_one",
    "LehmerPair.alpha_ne_zero",
    "LehmerPair.beta_ne_zero",
    "LehmerPair.alpha_ne_beta",
    "LehmerPair.oddDenominator_ne_zero",
    "LehmerPair.add_ne_zero",
    "LehmerPair.sq_sub_sq_ne_zero",
    "LehmerPair.coe_discriminant",
    "LehmerPair.coe_squaredEvenDenominator",
    "LehmerPair.term_one",
    "LehmerPair.term_two",
)
namespace = "Stage1.THM_M_0405."
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
assert output.count("M0405_PROOF_AXIOM_AUDIT_END") == 1
assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
assert "error:" not in output
PY

python3 "$target/check_proof.py"
printf '%s\n' \
  "PASS THM-M-0405 proof phase: 18 local normalization bodies elaborated with --trust=0" \
  "root remains open at M0405-X-BHV-BRIDGE; theorem_complete=false"
