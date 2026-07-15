#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
lean_root="$repo_root/Formalizations/Lean"
mathlib_root="$lean_root/.lake/packages/mathlib"
target_root="$repo_root/Stage1_Instances/THM-M-0711"
canonical_lake_root=$(cd "$lean_root/.lake" && pwd -P)
tmp=$(mktemp -d "$repo_root/.m0711-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

cp "$target_root/Statement.lean" "$target_root/ObligationTree.lean" \
  "$target_root/Proof.lean" "$tmp/"

# Reuse only the already pinned mathlib build closure and matching Lean binary.
# This avoids asking the top-level workspace to inspect unrelated dependencies
# and never repairs, updates, or otherwise mutates `.lake`.
lean_bin=$(cd "$mathlib_root" && lake env which lean)
lean_path=$(cd "$mathlib_root" && lake env printenv LEAN_PATH)
expected_lean_sha=3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf
actual_lean_sha=$(sha256sum "$lean_bin" | cut -d' ' -f1)
test "$actual_lean_sha" = "$expected_lean_sha"
lean_path=${lean_path//"$canonical_lake_root/packages/mathlib/.lake/packages"/"$canonical_lake_root/packages"}

LEAN_PATH="$lean_path" "$lean_bin" --trust=0 \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean_bin" --trust=0 \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$lean_path" "$lean_bin" --trust=0 "$tmp/Proof.lean"
