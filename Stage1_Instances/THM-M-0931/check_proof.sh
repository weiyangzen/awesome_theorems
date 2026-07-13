#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0931"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d "$lean_root/.stage1-m0931-proof.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_path="$(lake env printenv LEAN_PATH)"
relative_tmp="${tmp#"$lean_root"/}"
LEAN_PATH="$lean_path" lake env lean -o "$relative_tmp/Statement.olean" \
  "$relative_tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$lean_path" lake env lean -o "$relative_tmp/ObligationTree.olean" \
  "$relative_tmp/ObligationTree.lean" >/dev/null
LEAN_PATH="$tmp:$lean_path" lake env lean "$relative_tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Int.erdos_ginzburg_ziv_multiset",
    "Int.erdos_ginzburg_ziv",
    "char_dvd_card_solutions_of_add_lt",
    "Stage1Instances.THM_M_0931.Proof.pinnedIndexedIntegerEGZ",
    "Stage1Instances.THM_M_0931.Proof.pinnedAtLeastCountAnchor",
    "Stage1Instances.THM_M_0931.Proof.atLeastCountAnchor_via_frozen_enumeration",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_via_frozen_composition",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv_direct",
    "Stage1Instances.THM_M_0931.Proof.erdosGinzburgZiv",
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
PY
