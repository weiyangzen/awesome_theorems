#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 900s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1024"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1024-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 360 "$lean_bin" --trust=0 -R "$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean" >"$tmp/statement.out"

LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 480 "$lean_bin" --trust=0 -R "$target" \
    "$target/Proof.lean" >"$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
expected = {
    "Stage1Instances.THM_M_1024.integrable_compensatedIntegrand",
    "Stage1Instances.THM_M_1024.integrable_levyExponent_jump",
    "Stage1Instances.THM_M_1024.levyExponent_zero",
    "Stage1Instances.THM_M_1024.continuous_integral_compensatedIntegrand",
    "Stage1Instances.THM_M_1024.continuous_levyExponent",
}
allowed = {"propext", "Classical.choice", "Quot.sound"}
reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
names = {name for name, _ in reports}
assert names == expected, f"axiom-report coverage mismatch: {names}"
for name, raw in reports:
    actual = {part.strip() for part in raw.split(",") if part.strip()}
    assert actual == allowed, f"unexpected axioms for {name}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-1024 axiom closure: five exported bodies use only the allowed profile")
PY

python3 -B "$target/check_proof.py"
cat "$tmp/proof.out"
printf '%s\n' \
  'PASS THM-M-1024 pinned proof replay: ten local exponent declarations checked' \
  'closed frozen obligations: none; M1024-N-EXPONENT is partial' \
  'root closure: open (M3); theorem_complete=false'
