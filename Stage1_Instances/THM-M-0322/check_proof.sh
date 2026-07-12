#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
lean_root="$repo_root/Formalizations/Lean"
target_dir="$repo_root/Stage1_Instances/THM-M-0322"
tmp_dir=$(mktemp -d /tmp/thm-m-0322-proof.XXXXXX)
trap 'rm -rf "$tmp_dir"' EXIT

lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)

cd "$target_dir"
LEAN_PATH="$lean_path" "$lean" -o "$tmp_dir/Statement.olean" Statement.lean
LEAN_PATH="$tmp_dir:$lean_path" "$lean" -o "$tmp_dir/ObligationTree.olean" ObligationTree.lean
LEAN_PATH="$tmp_dir:$lean_path" "$lean" Proof.lean
