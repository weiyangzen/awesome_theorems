#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
lean_root="$repo_root/Formalizations/Lean"
target_root="$repo_root/Stage1_Instances/THM-M-0709"
tmp=$(mktemp -d "$lean_root/.m0709-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

cp "$target_root/Statement.lean" "$target_root/Proof.lean" "$tmp/"
cd "$lean_root"
lake env lean --trust=0 -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean --trust=0 "$tmp/Proof.lean"
