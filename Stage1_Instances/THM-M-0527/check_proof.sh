#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 600s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0527"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0527-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"
cp "$target/Statement.lean" "$target/Proof.lean" "$tmp"/

(
  cd "$tmp"
  LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
    timeout 240 "$lean_bin" --trust=0 -t0 -R "$tmp" \
      -o Statement.olean Statement.lean >statement.out
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
    timeout 300 "$lean_bin" --trust=0 -t0 -R "$tmp" \
      Proof.lean >proof.out
)

python3 -B "$target/check_proof.py" "$tmp/proof.out"
cat "$tmp/proof.out"
printf '%s\n' \
  'PASS THM-M-0527 pinned proof replay: fiber-classification branch checked' \
  'closed frozen obligations: none pending planned-signature reconciliation' \
  'root closure: open (M3); theorem_complete=false'
