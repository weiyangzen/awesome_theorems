#!/usr/bin/env bash
set -euo pipefail

lake env lean ../../Stage1_Instances/THM-M-0166/Proof.lean

if rg -n '\b(sorry|admit|axiom|unsafe)\b' \
  ../../Stage1_Instances/THM-M-0166/Proof.lean; then
  echo 'forbidden proof token found' >&2
  exit 7
fi

