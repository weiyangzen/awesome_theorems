#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-0590"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-0590-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
LEAN_PATH=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)

(
  cd "$TARGET"
  LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH" timeout 600 \
    "$LEAN" --trust=0 -t0 -o "$TMP/Statement.olean" Statement.lean
)
(
  cd "$TARGET"
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH" timeout 600 \
    "$LEAN" --trust=0 -t0 -o "$TMP/ObligationTree.olean" ObligationTree.lean
)
(
  cd "$TARGET"
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH" timeout 600 \
    "$LEAN" --trust=0 -t0 -o "$TMP/Proof.olean" Proof.lean
)

echo "PASS THM-M-0590 partial proof bodies"
