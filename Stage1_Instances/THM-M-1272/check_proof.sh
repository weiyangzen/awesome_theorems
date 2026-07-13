#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
target="$repo_root/Stage1_Instances/THM-M-1272"
lean_root="$repo_root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1272-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean_bin" --trust=0 -t0 -R "$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean_bin" --trust=0 -t0 -R "$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean_bin" --trust=0 -t0 -R "$target" "$target/Proof.lean"

python3 "$target/check_proof.py"
