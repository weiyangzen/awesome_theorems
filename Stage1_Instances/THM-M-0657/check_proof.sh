#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0657"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0657-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(env -u LEAN_PATH lake env which lean)"
lean_path="$(env -u LEAN_PATH lake env printenv LEAN_PATH)"
cd "$tmp"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -o Statement.olean Statement.lean >statement.out
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean \
  >obligation-tree.out
LEAN_NUM_THREADS=1 LEAN_PATH=".:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0657.hasModelCardinality_of_uncountably_categorical",
    "Stage1Instances.THM_M_0657.infinitePart_categorical",
    "Stage1Instances.THM_M_0657.infinitePart_isComplete",
    "Stage1Instances.THM_M_0657.categoricalWithExistence_of_categorical",
    "Stage1Instances.THM_M_0657.morleyCategoricityTarget_of_categoricalTransfer",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    no_axioms = f"'{declaration}' does not depend on any axioms" in output
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert no_axioms or match, f"missing axiom report for {declaration}"
    if match:
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output and "error:" not in output
PY

python3 "$target/check_proof.py"

printf '%s\n' \
  'PASS THM-M-0657 partial proof: existence and infinite-part completeness checked' \
  'provisional obligation closure: M0657-C-EXISTENCE and M0657-L-COMPLETENESS' \
  'root closure: open (M3); Morley categoricity-transfer core remains open'
