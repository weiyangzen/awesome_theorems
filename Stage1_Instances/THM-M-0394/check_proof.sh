#!/usr/bin/env bash
set -euo pipefail

statement_olean=../../Stage1_Instances/THM-M-0394/Statement.olean
tree_olean=../../Stage1_Instances/THM-M-0394/ObligationTree.olean
trap 'rm -f "$statement_olean" "$tree_olean"' EXIT

lake env lean -R ../.. -o "$statement_olean" \
  ../../Stage1_Instances/THM-M-0394/Statement.lean
LEAN_PATH=../.. lake env lean -R ../.. -o "$tree_olean" \
  ../../Stage1_Instances/THM-M-0394/ObligationTree.lean
LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-0394/Proof.lean
