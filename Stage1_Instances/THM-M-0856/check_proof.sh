#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0856"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0856-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"

cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" --trust=0 -o Statement.olean Statement.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 Proof.lean | tee proof.out

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "SimpleGraph.tutte",
    "Stage1Instances.THM_M_0856.Proof.pinnedTerminal",
    "Stage1Instances.THM_M_0856.Proof.tutteOneFactor_via_frozen_composition",
    "Stage1Instances.THM_M_0856.Proof.tutteOneFactor_direct",
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
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
PY
