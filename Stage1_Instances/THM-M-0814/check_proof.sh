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
target="$repo_root/Stage1_Instances/THM-M-0814"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0814-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"

LC_ALL=C LANG=C NO_COLOR=1 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 180 "$lean_bin" --trust=0 -o "$tmp/Statement.olean" \
    "$target/Statement.lean" > "$tmp/statement.out"

LC_ALL=C LANG=C NO_COLOR=1 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 180 "$lean_bin" --trust=0 -o "$tmp/ObligationTree.olean" \
    "$target/ObligationTree.lean" > "$tmp/obligation.out"

LC_ALL=C LANG=C NO_COLOR=1 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 180 "$lean_bin" --trust=0 -o "$tmp/Proof.olean" \
    "$target/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0814_Obligations.weakDuality_proof",
    "Stage1Instances.THM_M_0814_Obligations.noChain_case",
    "Stage1Instances.THM_M_0814_Obligations.cutCertificate_of_equalCut",
    "Stage1Instances.THM_M_0814_Obligations.root_of_maximalFlowAttainment_and_equalCut",
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
assert "Declarations are sorry-free!" in output
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-0814 isolated Lean replay: four local proof declarations checked")
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
