#!/usr/bin/env bash
set -euo pipefail

: "${STAGE1_LEAN_BIN:?missing pinned Lean executable}"
: "${STAGE1_LEAN_PATH:?missing pinned Lean path}"

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
target="$repo_root/Stage1_Instances/THM-M-1272"
tmp=$(/usr/bin/mktemp -d /tmp/thm-m-1272-release-lean.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

/usr/bin/cp "$target/Statement.lean" "$target/ObligationTree.lean" "$target/Proof.lean" "$tmp"/
LEAN_PATH="$STAGE1_LEAN_PATH" "$STAGE1_LEAN_BIN" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$STAGE1_LEAN_PATH" "$STAGE1_LEAN_BIN" --trust=0 -t0 -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" >/dev/null
output=$(LEAN_PATH="$tmp:$STAGE1_LEAN_PATH" "$STAGE1_LEAN_BIN" --trust=0 -t0 -R "$tmp" \
  "$tmp/Proof.lean")
printf '%s\n' "$output"
/usr/bin/python3 -I -B "$target/check_proof.py"
printf '%s\n' \
  "PASS THM-M-1272 release Lean replay: compactness package closed; symmetric minimax package remains explicit and open"
