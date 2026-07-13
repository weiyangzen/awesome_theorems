#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
lean_root="$repo_root/Formalizations/Lean"
target_root="$repo_root/Stage1_Instances/THM-M-1055"
tmp=$(mktemp -d "$lean_root/.m1055-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

cp "$target_root"/{Statement,ObligationTree,Proof}.lean "$tmp/"
cp "$target_root"/External/{MaximalErgodic,Birkhoff}.lean "$tmp/"

cd "$lean_root"
lake env lean -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -R "$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -R "$tmp" -o "$tmp/MaximalErgodic.olean" "$tmp/MaximalErgodic.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -R "$tmp" -o "$tmp/Birkhoff.olean" "$tmp/Birkhoff.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -R "$tmp" "$tmp/Proof.lean"
