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
target="$repo_root/Stage1_Instances/THM-M-1065"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1065-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 360 "$lean_bin" --trust=0 -t0 --root="$tmp" \
    -o "$tmp/Statement.olean" "$tmp/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 360 "$lean_bin" --trust=0 -t0 --root="$tmp" \
    "$tmp/Proof.lean" >"$tmp/proof.out" 2>&1
cat "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1065.exists_commonIIDSequences",
    "Stage1Instances.THM_M_1065.measurableSet_discrepancyEvent",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-1065 isolated Lean replay: two local partial proof bodies checked")
PY
