#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1227-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_root" && lake env which lean)
base_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)

mkdir -p "$tmp/Stage1_Instances/THM-M-1227"
cp "$here/Statement.lean" "$tmp/Stage1_Instances/THM-M-1227/Statement.lean"
cp "$here/Proof.lean" "$tmp/Stage1_Instances/THM-M-1227/Proof.lean"

cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" \
  timeout 300 "$lean" --trust=0 -t0 -R . \
  -o Stage1_Instances/THM-M-1227/Statement.olean \
  Stage1_Instances/THM-M-1227/Statement.lean > statement.out
LEAN_NUM_THREADS=1 LEAN_PATH=".:$base_path" \
  timeout 300 "$lean" --trust=0 -t0 -R . \
  Stage1_Instances/THM-M-1227/Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1.THM_M_1227.zero_isLerayHopfSolution",
    "Stage1.THM_M_1227.lerayHopfExistence_of_eq_zero",
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
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "error:" not in output
print("PASS THM-M-1227 isolated Lean replay: zero-data branch checked")
PY
