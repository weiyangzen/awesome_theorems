#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
lean_root="$repo_root/Formalizations/Lean"
toolchain="$(tr -d '\r\n' < "$lean_root/lean-toolchain")"
toolchain_name="${toolchain/:/---}"
toolchain_name="${toolchain_name//\//--}"
toolchain_bin="$HOME/.elan/toolchains/$toolchain_name/bin"
lake="$toolchain_bin/lake"

if [[ ! -x "$lake" ]]; then
  echo "missing pinned Lake binary: $lake" >&2
  exit 1
fi

cd "$lean_root"

echo "[1/7] build node-scoped statement/reduction and branch modules"
LAKE_NUM_JOBS="${LAKE_NUM_JOBS:-1}" "$lake" build \
  +AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.SmallExponentsPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.InternalCoveragePath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.Sample

echo "[2/7] build the Stage1 integration wrapper"
LAKE_NUM_JOBS="${LAKE_NUM_JOBS:-1}" "$lake" build \
  +AwesomeTheorems.Stage1.S1_M_001

echo "[3/7] check theorem-folder sample"
"$lake" env lean ../../THM-M-0387/FermatLastTheorem_Sample.lean

echo "[4/7] build the shared AwesomeTheorems aggregator"
LAKE_NUM_JOBS="${LAKE_NUM_JOBS:-1}" "$lake" build +AwesomeTheorems

echo "[5/7] run the full local Lake build"
LAKE_NUM_JOBS="${LAKE_NUM_JOBS:-1}" "$lake" build

echo "[6/7] compile the rev-5.6 dossier lint"
cd "$repo_root"
python3 -m py_compile scripts/lint_theorem_dossier.py

echo "[7/7] lint rev-5.6 tree, evidence, pins, public surfaces, and Lean probes"
python3 scripts/lint_theorem_dossier.py THM-M-0387
