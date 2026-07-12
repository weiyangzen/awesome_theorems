#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/Stage1_Instances/THM-M-0985"
lean_root="$root/Formalizations/Lean"
tmp="$(mktemp -d "$target/.proof-check.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/Proof.lean" "$tmp/"

base_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
(
  cd "$tmp"
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$base_path" \
    lake env lean -o Statement.olean Statement.lean
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH=".:$base_path" \
    lake env lean -o ObligationTree.olean ObligationTree.lean
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH=".:$base_path" \
    lake env lean Proof.lean
)

if rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b|sorryAx' \
    "$target/Proof.lean"; then
  echo "prohibited proof construct detected" >&2
  exit 1
fi

echo "PASS THM-M-0985 proof: pinned terminal package and exact root elaborate"
