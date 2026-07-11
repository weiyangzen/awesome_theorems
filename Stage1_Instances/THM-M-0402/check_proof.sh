#!/usr/bin/env bash
set -euo pipefail

tmp=$(mktemp -d ./.m0402-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

cp ../../Stage1_Instances/THM-M-0402/Statement.lean \
  ../../Stage1_Instances/THM-M-0402/Proof.lean "$tmp/"
lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" \
  lake env lean "$tmp/Proof.lean"
