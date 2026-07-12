#!/usr/bin/env bash
set -euo pipefail

target_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$target_dir/../.." && pwd)"
lean_project="$repo_root/Formalizations/Lean"
tmp_dir="$(mktemp -d /tmp/thm-m-0646-proof.XXXXXX)"
trap 'rm -rf "$tmp_dir"' EXIT

lean_path="$(cd "$lean_project" && lake env printenv LEAN_PATH)"

cd "$target_dir"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$lean_path" \
  lake env lean -o "$tmp_dir/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$tmp_dir:$lean_path" \
  lake env lean Proof.lean

if rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b|sorryAx|implemented_by' \
    Proof.lean; then
  echo "forbidden proof boundary found" >&2
  exit 1
fi

echo "PASS THM-M-0646 proof phase: exact pinned wrapper elaborated"
