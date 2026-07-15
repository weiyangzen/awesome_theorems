#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 300s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1070"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1070-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1070"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 240 "$lean_bin" --trust=0 -R "$repo_root" \
    -o "$tmp/Stage1_Instances/THM-M-1070/Statement.olean" \
    "$target/Statement.lean" >"$tmp/statement.out"

LEAN_NUM_THREADS=1 LEAN_PATH="$tmp/Stage1_Instances/THM-M-1070:$lean_path" \
  timeout 240 "$lean_bin" --trust=0 -R "$repo_root" \
    -o "$tmp/Proof.olean" "$target/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1070.isLevyProcess_of_clauses",
    "Stage1Instances.THM_M_1070.clauses_of_isLevyProcess",
    "Stage1Instances.THM_M_1070.isLevyProcess_zero",
    "Stage1Instances.THM_M_1070.zeroMeasure_not_isLevyProcess",
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
print("PASS THM-M-1070 isolated Lean replay: four local proof declarations checked")
PY
