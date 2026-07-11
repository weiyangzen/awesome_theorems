#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
lean_root=$(cd "$here/../../Formalizations/Lean" && pwd)
lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
tmp=$(mktemp -d "$here/.proof-check.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

cp "$here"/{Statement,ObligationTree,Proof}.lean "$tmp/"
LEAN_PATH="$lean_path" "$lean_bin" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean_bin" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$lean_path" "$lean_bin" "$tmp/Proof.lean"
