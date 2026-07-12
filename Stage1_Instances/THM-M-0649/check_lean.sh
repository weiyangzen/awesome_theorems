#!/usr/bin/env bash
set -euo pipefail

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

lake env lean -R ../../Stage1_Instances/THM-M-0649 \
  -o "$tmp_dir/Statement.olean" \
  ../../Stage1_Instances/THM-M-0649/Statement.lean
LEAN_PATH="$tmp_dir" lake env lean -R ../../Stage1_Instances/THM-M-0649 \
  -o "$tmp_dir/ObligationTree.olean" \
  ../../Stage1_Instances/THM-M-0649/ObligationTree.lean
LEAN_PATH="$tmp_dir" lake env lean \
  ../../Stage1_Instances/THM-M-0649/Proof.lean
