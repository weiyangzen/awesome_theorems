#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m0395-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-0395"
cp ../../Stage1_Instances/THM-M-0395/{Statement,Proof}.lean \
  "$tmp/Stage1_Instances/THM-M-0395/"

lean_path=$(lake env printenv LEAN_PATH)
lean_bin=$(lake env printenv LEAN)

LEAN_PATH="$lean_path" "$lean_bin" --trust=0 \
  -o "$tmp/Stage1_Instances/THM-M-0395/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-0395/Statement.lean"
LEAN_PATH="$tmp:$lean_path" "$lean_bin" --trust=0 \
  "$tmp/Stage1_Instances/THM-M-0395/Proof.lean"
