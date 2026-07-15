#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0325"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0325-proof-slot35.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

lake_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lake"
test -x "$lake_bin"
tool_probe="$tmp/tool-probe"
mkdir "$tool_probe"
cp "$lean_root/lean-toolchain" "$tool_probe/"
# Use pinned Lake in a manifest-free probe so the broken unrelated dependency
# cannot trigger resolution or a fetch.
lean_bin="$(cd "$tool_probe" && "$lake_bin" env which lean)"
"$lean_bin" --version
lean_path="$(find "$lean_root/.lake/packages" -path '*/.lake/build/lib/lean' -type d -print | sort | paste -sd: -)"
test -n "$lean_path"

cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/AnchorAudit.lean" "$target/Proof.lean" "$tmp/"
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 900 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 900 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >"$tmp/obligation-tree.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 900 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/AnchorAudit.olean" \
  "$tmp/AnchorAudit.lean" >"$tmp/anchor-audit.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 900 \
  "$lean_bin" --trust=0 -t0 --root="$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean" >"$tmp/proof.out" 2>&1

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "scalarUnitBoundedBy_apply",
    "scalarUnitBoundedBy_of_abs_eq_one",
    "nonneg_of_scalarUnitBoundedBy",
    "scalarMatrixForm_zero",
    "hilbertMatrixForm_zero",
    "zero_scalarUnitBoundedBy",
    "zero_hilbertUnitBoundedBy",
    "abs_real_inner_le_one_of_norm_le_one",
    "abs_matrix_inner_term_le",
    "abs_hilbertMatrixForm_le_sum_abs",
    "hilbertUnitBoundedBy_sum_abs",
)
namespace = "Stage1Instances.THM_M_0325."
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
assert "sorryAx" not in output and "declaration uses 'sorry'" not in output
assert "error:" not in output
PY

sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" \
  "$tmp/AnchorAudit.olean" "$tmp/Proof.olean"
python3 "$target/check_proof.py"
printf '%s\n' \
  "PASS THM-M-0325 proof phase: 11 local scalar/Hilbert boundary bodies elaborated with --trust=0" \
  "root remains open at M0325-T-PACKAGE; theorem_complete=false"
