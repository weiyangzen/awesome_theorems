#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-0612"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-0612-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
LEAN_PATH=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)

(
  cd "$TARGET"
  LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH" timeout --foreground 600 \
    "$LEAN" --trust=0 -t0 -o "$TMP/Statement.olean" Statement.lean
)
(
  cd "$TARGET"
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH" timeout --foreground 600 \
    "$LEAN" --trust=0 -t0 -o "$TMP/LocalEncoding.olean" LocalEncoding.lean
)
(
  cd "$TARGET"
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH" timeout --foreground 600 \
    "$LEAN" --trust=0 -t0 -o "$TMP/DimensionTwo.olean" DimensionTwo.lean
)

echo "PASS THM-M-0612 dimension-two proof bodies"
