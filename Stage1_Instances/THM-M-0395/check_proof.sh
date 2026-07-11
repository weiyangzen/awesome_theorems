#!/usr/bin/env bash
set -euo pipefail

statement_olean=../../Stage1_Instances/THM-M-0395/Statement.olean
trap 'rm -f "$statement_olean"' EXIT

lake env lean -R ../.. -o "$statement_olean" \
  ../../Stage1_Instances/THM-M-0395/Statement.lean
LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-0395/Proof.lean
