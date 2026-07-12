#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1268"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$target/Statement.lean" "$target/Proof.lean" "$target/ProofExact.lean" "$tmp/"

cd "$lean_root"
lake env lean -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
lake env lean -R "$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean"
lean_path="$(lake env printenv LEAN_PATH)"
LEAN_PATH="$tmp:$lean_path" lake env lean "$tmp/ProofExact.lean"

