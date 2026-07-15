#!/usr/bin/env bash
set -euo pipefail

export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export TZ=UTC
export LEAN_NUM_THREADS=1

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0353"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d "${TMPDIR:-/tmp}/thm-m-0353-proof.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

if (( $# != 0 )); then
  printf 'usage: %s\n' "$0" >&2
  exit 2
fi

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"
cp -R "$target/Vendor" "$tmp/Vendor"

lean_bin="$(
  cd "$lean_root"
  env -u LEAN_PATH lake env which lean
)"
base_lean_path="$(
  cd "$lean_root"
  env -u LEAN_PATH lake env printenv LEAN_PATH
)"
test -x "$lean_bin"
test -n "$base_lean_path"

run_lean() {
  local lean_path=$1
  local source=$2
  local output=$3
  local log=$4

  LEAN_PATH="$lean_path" timeout --foreground --kill-after=10s 1800s \
    "$lean_bin" --trust=0 -t0 -R "$tmp" -o "$output" "$source" \
    >"$log" 2>&1
}

run_lean "$base_lean_path" \
  "$tmp/Statement.lean" "$tmp/Statement.olean" "$tmp/statement.out"
run_lean "$tmp:$base_lean_path" \
  "$tmp/ObligationTree.lean" "$tmp/ObligationTree.olean" "$tmp/obligation-tree.out"
run_lean "$base_lean_path" \
  "$tmp/Vendor/GaussianField/HermiteFunctions.lean" \
  "$tmp/Vendor/GaussianField/HermiteFunctions.olean" "$tmp/vendor.out"
run_lean "$tmp:$base_lean_path" \
  "$tmp/Proof.lean" "$tmp/Proof.olean" "$tmp/proof.out"

python3 -B - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
expected = {
    "hermiteFunction_memLp",
    "hermiteFunction_orthonormal",
    "hermiteFunction_complete",
    "Stage1Instances.THM_M_0353.hermiteMemLpPackage_proof",
    "Stage1Instances.THM_M_0353.hermiteBasisPackage_proof",
    "Stage1Instances.THM_M_0353.hermiteCompletenessTarget_proof",
}
allowed = ["propext", "Classical.choice", "Quot.sound"]

if output.count("Declarations are sorry-free!") != len(expected):
    raise SystemExit("FAIL: expected six sorry-free declaration reports")

reports = re.findall(
    r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL
)
reported = {name for name, _ in reports}
if len(reports) != len(expected) or reported != expected:
    raise SystemExit(
        "FAIL: axiom-report coverage mismatch: "
        f"missing={sorted(expected - reported)}, extra={sorted(reported - expected)}"
    )

for name, raw_axioms in reports:
    actual = [part.strip() for part in raw_axioms.split(",") if part.strip()]
    if actual != allowed:
        raise SystemExit(f"FAIL: unexpected axioms for {name}: {actual}")

for prohibited in ("sorryAx", "declaration uses 'sorry'", "error:"):
    if prohibited in output:
        raise SystemExit(f"FAIL: prohibited Lean output: {prohibited}")
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Vendor/GaussianField/HermiteFunctions.olean"
test -s "$tmp/Proof.olean"

printf '%s\n' \
  'PASS THM-M-0353 isolated trust-zero proof replay: four modules elaborated' \
  'PASS six declarations sorry-free; axioms exactly [propext, Classical.choice, Quot.sound]'
