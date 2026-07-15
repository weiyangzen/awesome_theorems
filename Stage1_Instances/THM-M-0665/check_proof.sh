#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
target="$root/Stage1_Instances/THM-M-0665"
lean_project="$root/Formalizations/Lean"
tmp=$(mktemp)
trap 'rm -f "$tmp"' EXIT

{
  sed -n '/^import /p' "$target/Statement.lean"
  echo 'import Mathlib.Util.AssertNoSorry'
  sed '/^import /d' "$target/Statement.lean"
  sed '/^import /d' "$target/Proof.lean"
} | (
  cd "$lean_project"
  env -u LEAN_PATH LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 180s \
    lake env lean --trust=0 -j1 -t0 /dev/stdin
) >"$tmp" 2>&1

cat "$tmp"

if grep -Eq 'declaration uses .sorry.|sorryAx' "$tmp"; then
  echo "FAIL: Lean reported a placeholder" >&2
  exit 1
fi

echo "PASS THM-M-0665 isolated trust-zero statement and partial proof elaboration"
