#!/usr/bin/env bash
set -euo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
lean_root="$here/../../Formalizations/Lean"
tmp="$(mktemp -d "$lean_root/.m0417-proof.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

cp "$here"/{Statement,ObligationTree,Proof}.lean "$tmp"/
cd "$lean_root"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" >/dev/null
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$tmp/Proof.lean" | awk '
    /^Stage1Instances\.THM_M_0417\.Proof\./ ||
    /^.MeasureTheory\.exists_/ ||
    /depends on axioms/ ||
    /^[[:space:]]+(Classical\.choice|Quot\.sound)/
  '

cd "$here/../.."
python3 Stage1_Instances/THM-M-0417/check_proof.py
