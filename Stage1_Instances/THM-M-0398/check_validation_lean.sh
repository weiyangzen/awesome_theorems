#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m0398-validation.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp ../../Stage1_Instances/THM-M-0398/{Statement,ObligationTree,Validation}.lean "$tmp/"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$tmp/Validation.lean"
