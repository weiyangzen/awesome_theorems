#!/usr/bin/env bash
set -euo pipefail

repo=$(cd "$(dirname "$0")/../.." && pwd)
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d "$lean_root/.m0981-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

cp "$repo/Stage1_Instances/THM-M-0981/Statement.lean" \
  "$repo/Stage1_Instances/THM-M-0981/ObligationTree.lean" \
  "$repo/Stage1_Instances/THM-M-0981/Proof.lean" "$tmp/"

cd "$lean_root"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
lean_path="$tmp:$(lake env printenv LEAN_PATH)"
LEAN_PATH="$lean_path" lake env lean -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" lake env lean "$tmp/Proof.lean"

cd "$repo"
python3 Stage1_Instances/THM-M-0981/check_proof.py
