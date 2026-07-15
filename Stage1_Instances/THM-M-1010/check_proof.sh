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

export LC_ALL=C.UTF-8
export TZ=Asia/Shanghai
export LEAN_NUM_THREADS=1

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
lean_root="$repo_root/Formalizations/Lean"
target="$repo_root/Stage1_Instances/THM-M-1010"
tmp="$(mktemp -d /tmp/stage1-m1010-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"
version="$($lean_bin --version)"
case "$version" in
  *'version 4.29.0'*'commit 98dc76e3c0a9b856c9b98726b713fb04fab16740'*) ;;
  *) printf 'FAIL: unexpected Lean executable: %s\n' "$version" >&2; exit 1 ;;
esac

LEAN_PATH="$lean_path" timeout 240 "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  "$target/ObligationTree.lean" >"$tmp/obligation.out" 2>&1
LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  "$target/Proof.lean" >"$tmp/proof.out" 2>&1
cat "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1010.representation_of_constant_laws",
    "Stage1Instances.THM_M_1010.target_for_constant_sequence",
    "Stage1Instances.THM_M_1010.exists_common_space_exact_marginals",
)
allowed = ["propext", "Classical.choice", "Quot.sound"]
reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
by_name = {
    name: [part.strip() for part in raw.split(",") if part.strip()]
    for name, raw in reports
}
assert set(by_name) == set(declarations), (
    f"axiom-report coverage mismatch: expected={declarations}, actual={tuple(by_name)}"
)
for declaration in declarations:
    assert by_name[declaration] == allowed, (
        f"unexpected axiom closure for {declaration}: {by_name[declaration]}"
    )
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", output)
print("PASS THM-M-1010 trust-zero replay: common marginals and boundary bodies checked")
PY

sha256sum "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
  "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean"
printf '%s\n' \
  'closed frozen obligations added: none; root remains open M3' \
  'proof_phase_complete=false; theorem_complete=false; accepted state unchanged'
