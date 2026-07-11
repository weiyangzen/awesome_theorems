#!/usr/bin/env bash
set -euo pipefail
trap 'rm -f ../../Stage1_Instances/THM-M-0394/Statement.olean' EXIT
lake env lean -R ../.. -o ../../Stage1_Instances/THM-M-0394/Statement.olean \
  ../../Stage1_Instances/THM-M-0394/Statement.lean
LEAN_PATH=../.. lake env lean ../../Stage1_Instances/THM-M-0394/ObligationTree.lean
