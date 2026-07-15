#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0669"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0669-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,Proof}.lean "$tmp/"

toolchain="$(tr -d '\r\n' < "$lean_root/lean-toolchain")"
toolchain_key="${toolchain//\//--}"
toolchain_key="${toolchain_key//:/---}"
lean_bin="${ELAN_HOME:-$HOME/.elan}/toolchains/$toolchain_key/bin/lean"
test -x "$lean_bin"
actual_version="$("$lean_bin" --version)"
case "$actual_version" in
  *"version 4.29.0"*"commit 98dc76e3c0a9b856c9b98726b713fb04fab16740"*) ;;
  *) echo "unexpected Lean toolchain for $toolchain: $actual_version" >&2; exit 1 ;;
esac
lean_path="$lean_root/.lake/build/lib/lean"
for package in batteries Qq aesop proofwidgets importGraph plausible LeanSearchClient; do
  package_lib="$lean_root/.lake/packages/$package/.lake/build/lib/lean"
  test -d "$package_lib"
  lean_path="$lean_path:$package_lib"
done
lean_path="$lean_path:$lean_root/.lake/packages/mathlib/.lake/build/lib/lean"
cd "$tmp"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -o Statement.olean Statement.lean >statement.out
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1.THM_M_0669.qfEquivalent_of_isQF",
    "Stage1.THM_M_0669.atomicEqualityNormalization",
    "Stage1.THM_M_0669.realize_polynomialOfTerm",
    "Stage1.THM_M_0669.atomicPolynomialNormalization",
    "Stage1.THM_M_0669.qfBooleanClosure",
    "Stage1.THM_M_0669.formulaElimination_of_oneVariable",
    "Stage1.THM_M_0669.tarskiQuantifierElimination_of_oneVariable",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    no_axioms = f"'{declaration}' does not depend on any axioms" in output
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert no_axioms or match, f"missing axiom report for {declaration}"
    if match:
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output and "error:" not in output
PY

python3 "$target/check_proof.py"

printf '%s\n' \
  'PASS THM-M-0669 partial proof: atomic, Boolean, and conditional recursion bodies checked' \
  'provisional closure: M0669-C-BOOLEAN; atomic normalization is partial progress' \
  'root closure: open (M3); algebraic one-variable elimination remains open'
