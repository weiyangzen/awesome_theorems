#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/Stage1_Instances/THM-M-1138"
TMP=$(mktemp -d /tmp/thm-m-1138-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

LEAN_BIN=$(cd "$ROOT/Formalizations/Lean" && lake env which lean)
LEAN_PATH_PINNED=$(cd "$ROOT/Formalizations/Lean" && lake env printenv LEAN_PATH)

cd "$ROOT"
LEAN_PATH="$LEAN_PATH_PINNED" "$LEAN_BIN" -R "$HERE" \
  "$HERE/Statement.lean" -o "$TMP/Statement.olean" >/dev/null
LEAN_PATH="$TMP:$LEAN_PATH_PINNED" "$LEAN_BIN" -R "$HERE" \
  "$HERE/ObligationTree.lean" -o "$TMP/ObligationTree.olean" >/dev/null
LEAN_PATH="$TMP:$LEAN_PATH_PINNED" "$LEAN_BIN" -R "$HERE" "$HERE/Proof.lean"
