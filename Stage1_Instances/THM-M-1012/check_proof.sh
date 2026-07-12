#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEAN_ROOT="$(cd "$HERE/../../Formalizations/Lean" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

BASE_LEAN_PATH="$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)"
export ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0

cd "$HERE"
LEAN_PATH="$BASE_LEAN_PATH" lake env lean -o "$TMP/Statement.olean" Statement.lean
LEAN_PATH="$BASE_LEAN_PATH" lake env lean -o "$TMP/ObligationTree.olean" ObligationTree.lean
LEAN_PATH="$TMP:$BASE_LEAN_PATH" lake env lean Proof.lean
