#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1255-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

cp "$here"/{Statement,ObligationTree,Proof}.lean "$tmp/"
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 -o Statement.olean Statement.lean >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 Proof.lean
