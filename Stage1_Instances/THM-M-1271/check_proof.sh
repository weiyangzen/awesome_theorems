#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1271"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-1271-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && timeout 120 lake env which lean)"
lean_path="$(cd "$lean_root" && timeout 120 lake env printenv LEAN_PATH)"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean" >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$target" \
  -o "$tmp/ObligationTree.olean" "$target/ObligationTree.lean" \
  >"$tmp/obligation-tree.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$target" "$target/Proof.lean" \
  >"$tmp/proof.out" 2>&1

cat "$tmp/obligation-tree.out" "$tmp/proof.out"

python3 - "$tmp/obligation-tree.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = "\n".join(Path(path).read_text(encoding="utf-8") for path in sys.argv[1:])
declarations = (
    "Stage1Instances.THM_M_1271.root_of_barrier_and_critical_packages",
    "Stage1Instances.THM_M_1271.admissiblePath_meets_sphere",
    "Stage1Instances.THM_M_1271.alpha_le_pathHeight",
    "Stage1Instances.THM_M_1271.pathHeight_attained",
    "Stage1Instances.THM_M_1271.mountainPassBarrierPackage",
    "Stage1Instances.THM_M_1271.exists_valueSequence_at_mountainPassLevel",
    "Stage1Instances.THM_M_1271.exists_criticalPoint_of_psSequence",
    "Stage1Instances.THM_M_1271.mountainPassCriticalPackage_of_psSequence",
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
  'PASS THM-M-1271 partial proof: path-height attainment and value convergence checked' \
  'closed frozen obligation: M1271-C-PATH-MAX (provisional)' \
  'root closure: open (M2); derivative-small Palais-Smale construction remains open'
