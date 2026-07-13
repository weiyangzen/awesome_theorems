#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0484"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0484-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" --trust=0 -o Statement.olean Statement.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "lucas_lehmer_sufficiency",
    "lucas_lehmer_necessity",
    "Stage1Instances.THM_M_0484.Proof.pinnedSufficiency",
    "Stage1Instances.THM_M_0484.Proof.pinnedNecessity",
    "Stage1Instances.THM_M_0484.Proof.assembledRoot",
    "Stage1Instances.THM_M_0484.Proof.lucasLehmerCriterion",
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
assert output.count("Declarations are sorry-free!") == 1
assert "sorryAx" not in output
PY
