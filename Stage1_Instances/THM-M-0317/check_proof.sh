#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0317"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0317-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && timeout 300 lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean" \
  >"$tmp/obligation-tree.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -R "$target" "$target/Proof.lean" \
  >"$tmp/proof.out" 2>&1

cat "$tmp/obligation-tree.out" "$tmp/proof.out"

python3 - "$tmp/obligation-tree.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = "\n".join(Path(path).read_text(encoding="utf-8") for path in sys.argv[1:])
declarations = (
    "AwesomeTheorems.THM_M_0317.root_of_approximation_and_limit",
    "AwesomeTheorems.THM_M_0317.zero_mem_closure_displacement_image",
    "AwesomeTheorems.THM_M_0317.isClosed_displacement_image",
    "AwesomeTheorems.THM_M_0317.compactnessLimitPackage",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    no_axioms = f"'{declaration}' does not depend on any axioms" in output
    assert match or no_axioms, f"missing axiom report for {declaration}"
    if match:
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "error:" not in output
PY

python3 "$target/check_proof.py"

printf '%s\n' \
  'PASS THM-M-0317 partial proof: exact compactness-limit package checked' \
  'provisionally closed: M0317-N-NEIGHBORHOODS, M0317-L-COMPACT-LIMIT, M0317-T-LIMIT' \
  'root closure: open (M2); M0317-T-APPROX remains open'
