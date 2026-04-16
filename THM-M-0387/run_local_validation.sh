#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
lean_root="$repo_root/Formalizations/Lean"
cd "$lean_root"

echo "[1/2] build split shared modules and aggregator"
LAKE_NUM_JOBS=1 ~/.elan/bin/lake build \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path \
  +AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath \
  +AwesomeTheorems.NumberTheory.THM_M_0387.Sample

echo "[2/2] check theorem-folder sample"
~/.elan/bin/lake env lean ../../THM-M-0387/FermatLastTheorem_Sample.lean
