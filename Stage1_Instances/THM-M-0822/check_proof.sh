#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
lean_root="$repo_root/Formalizations/Lean"
target_root="$repo_root/Stage1_Instances/THM-M-0822"
tmp=$(mktemp -d /tmp/thm-m-0822-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
lean_log="$tmp/Proof.log"

export LEAN_NUM_THREADS=1
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
export TZ=UTC

env -u THM_M_0822_LEAN_LOG LEAN_PATH="$lean_path" "$lean_bin" -j 1 \
  "$target_root/Statement.lean" -o "$tmp/Statement.olean" >/dev/null
env -u THM_M_0822_LEAN_LOG LEAN_PATH="$tmp:$lean_path" "$lean_bin" -j 1 \
  "$target_root/ObligationTree.lean" -o "$tmp/ObligationTree.olean" >/dev/null
env -u THM_M_0822_LEAN_LOG LEAN_PATH="$tmp:$lean_path" "$lean_bin" -j 1 \
  "$target_root/Proof.lean" 2>&1 | tee "$lean_log"

THM_M_0822_LEAN_LOG="$lean_log" python3 -B "$target_root/check_proof.py"
