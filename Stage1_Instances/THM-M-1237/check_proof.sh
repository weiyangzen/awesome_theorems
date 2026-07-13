#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1237-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

cd "$lean_root"
lake env lean -R "$here" -o "$tmp/Statement.olean" "$here/Statement.lean"
LEAN_PATH="$tmp:${LEAN_PATH:-}" lake env lean -R "$here" \
  -o "$tmp/ObligationTree.olean" "$here/ObligationTree.lean"
LEAN_PATH="$tmp:${LEAN_PATH:-}" lake env lean "$here/Proof.lean"
