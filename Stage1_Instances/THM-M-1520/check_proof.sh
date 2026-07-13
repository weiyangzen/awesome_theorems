#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
HERE="$ROOT/Stage1_Instances/THM-M-1520"
TMP=$(mktemp -d /tmp/thm-m-1520-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

if LEAN_BIN=$(cd "$ROOT/Formalizations/Lean" && lake env which lean 2>/dev/null) &&
    LEAN_PATH_PINNED=$(cd "$ROOT/Formalizations/Lean" && lake env printenv LEAN_PATH 2>/dev/null); then
  :
else
  TOOLCHAIN=$(sed 's#/#--#g; s#:#---#g' "$ROOT/Formalizations/Lean/lean-toolchain")
  LEAN_BIN="$HOME/.elan/toolchains/$TOOLCHAIN/bin/lean"
  LEAN_PATH_PINNED=$(find "$ROOT/Formalizations/Lean/.lake/packages" -maxdepth 5 -type d \
    -path '*/.lake/build/lib/lean' -print | sort | paste -sd: -)
  LEAN_PATH_PINNED="$LEAN_PATH_PINNED:$ROOT/Formalizations/Lean/.lake/build/lib/lean"
fi

test -x "$LEAN_BIN"
test -n "$LEAN_PATH_PINNED"

cp "$HERE"/{Statement,Proof,FlowAlgebra,JacobianBridge,VectorFieldRegularity,ChangeOfVariables,ObligationTree}.lean "$TMP/"

run_base() {
  LEAN_NUM_THREADS=1 LEAN_PATH="$LEAN_PATH_PINNED" timeout 300 \
    "$LEAN_BIN" --trust=0 -t0 "$@"
}

run_local() {
  LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$LEAN_PATH_PINNED" timeout 300 \
    "$LEAN_BIN" --trust=0 -t0 "$@"
}

cd "$TMP"
run_base -o Statement.olean Statement.lean >/dev/null
run_local -o Proof.olean Proof.lean
run_local -o FlowAlgebra.olean FlowAlgebra.lean
run_base -o JacobianBridge.olean JacobianBridge.lean
run_local -o VectorFieldRegularity.olean VectorFieldRegularity.lean
run_local -o ChangeOfVariables.olean ChangeOfVariables.lean
run_local -o ObligationTree.olean ObligationTree.lean
