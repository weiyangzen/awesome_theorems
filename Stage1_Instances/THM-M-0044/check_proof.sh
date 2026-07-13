#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
out="/tmp/stage1-thm-m-0044-proof-lean"

rm -rf "$out"
mkdir -p "$out"

lake env lean --root=../.. "$root/Stage1_Instances/THM-M-0044/Statement.lean" \
  -o "$out/Statement.olean"

LEAN_PATH="$out:$(lake env printenv LEAN_PATH)" \
  lake env lean --root=../.. "$root/Stage1_Instances/THM-M-0044/ObligationTree.lean" \
    -o "$out/ObligationTree.olean"

LEAN_PATH="$out:$(lake env printenv LEAN_PATH)" \
  lake env lean --root=../.. "$root/Stage1_Instances/THM-M-0044/Proof.lean"
