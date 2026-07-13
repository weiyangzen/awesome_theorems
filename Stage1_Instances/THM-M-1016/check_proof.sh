#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
LEAN_ROOT="$ROOT/Formalizations/Lean"
HERE="$ROOT/Stage1_Instances/THM-M-1016"
TMP_PARENT=${TMPDIR:-"$ROOT"}
TMP=$(mktemp -d "$TMP_PARENT/stage1-m1016-proof.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

cp "$HERE"/{Statement,ObligationTree,Proof}.lean "$TMP"/
LEAN_BIN=$(cd "$LEAN_ROOT" && lake env which lean)
LEAN_PATH_BASE=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)

(cd "$TMP" && LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_BASE" \
  "$LEAN_BIN" -o Statement.olean Statement.lean >/dev/null)
(cd "$TMP" && LEAN_NUM_THREADS=1 LEAN_PATH=".:$LEAN_PATH_BASE" \
  "$LEAN_BIN" -o ObligationTree.olean ObligationTree.lean >/dev/null)
OUTPUT=$(cd "$TMP" && LEAN_NUM_THREADS=1 LEAN_PATH=".:$LEAN_PATH_BASE" \
  "$LEAN_BIN" Proof.lean 2>&1)
printf '%s\n' "$OUTPUT"

COUNT=$(printf '%s\n' "$OUTPUT" | grep -F -c "depends on axioms:" || true)
if [[ "$COUNT" -ne 7 ]]; then
  printf 'expected seven axiom reports, found %s\n' "$COUNT" >&2
  exit 1
fi
RESIDUAL=$(printf '%s\n' "$OUTPUT" | sed -E \
  "s/'[^']+' depends on axioms://g; s/propext//g; s/Classical\.choice//g; s/Quot\.sound//g" | \
  tr -d '[],[:space:]')
if [[ -n "$RESIDUAL" ]]; then
  printf 'unexpected output or axiom closure in proof output: %s\n' "$RESIDUAL" >&2
  exit 1
fi
