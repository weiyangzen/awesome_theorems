#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m0082-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-0082"
cp ../../Stage1_Instances/THM-M-0082/{Statement,ObligationTree,Proof}.lean \
  "$tmp/Stage1_Instances/THM-M-0082/"

lake env lean \
  -o "$tmp/Stage1_Instances/THM-M-0082/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-0082/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean \
  -o "$tmp/Stage1_Instances/THM-M-0082/ObligationTree.olean" \
  "$tmp/Stage1_Instances/THM-M-0082/ObligationTree.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean \
  "$tmp/Stage1_Instances/THM-M-0082/Proof.lean"
