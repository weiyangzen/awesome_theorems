#!/usr/bin/env bash
set -euo pipefail

target_dir="$(cd "$(dirname "$0")" && pwd)"
lean_dir="$(cd "$target_dir/../../Formalizations/Lean" && pwd)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$target_dir"/{Statement,ObligationTree,Proof}.lean "$tmp/"
base_lean_path="$(cd "$lean_dir" && lake env printenv LEAN_PATH)"
lean="$(cd "$lean_dir" && lake env which lean)"

cd "$tmp"
LEAN_PATH="$base_lean_path" "$lean" -o Statement.olean Statement.lean
LEAN_PATH=".:$base_lean_path" "$lean" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$base_lean_path" "$lean" Proof.lean
