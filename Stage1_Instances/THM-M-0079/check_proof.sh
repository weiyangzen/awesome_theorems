#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0079"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d -p "$lean_root" .m0079-proof-check.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
LEAN_PATH="$lean_path" "$lean_bin" -o "$tmp/Statement.olean" "$tmp/Statement.lean" \
  > "$tmp/statement.out" 2>&1
LEAN_PATH="$tmp:$lean_path" "$lean_bin" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" > "$tmp/obligation-tree.out" 2>&1
LEAN_PATH="$tmp:$lean_path" "$lean_bin" "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "subgroupIsFreeOfIsFree",
    "Stage1Instances.THM_M_0079.Proof.quotientActionPretransitive",
    "Stage1Instances.THM_M_0079.Proof.quotientNonempty",
    "Stage1Instances.THM_M_0079.Proof.actionGroupoidFreeConstructor",
    "Stage1Instances.THM_M_0079.Proof.connectedFreeEndConstructor",
    "Stage1Instances.THM_M_0079.Proof.stabilizerEndConstructor",
    "Stage1Instances.THM_M_0079.Proof.quotientStabilizerIdentification",
    "Stage1Instances.THM_M_0079.Proof.mulEquivFreenessTransport",
    "Stage1Instances.THM_M_0079.Proof.quotientActionConnected",
    "Stage1Instances.THM_M_0079.Proof.endSubgroupEquivConstructor",
    "Stage1Instances.THM_M_0079.Proof.quotientVertexEndFree",
    "Stage1Instances.THM_M_0079.Proof.exactAssembly",
    "Stage1Instances.THM_M_0079.Proof.nielsenSchreier_via_frozen_composition",
    "Stage1Instances.THM_M_0079.Proof.nielsenSchreier_direct",
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
assert "sorryAx" not in output and "error:" not in output
print("PASS THM-M-0079 Lean proof: exact direct and frozen-composition roots are sorry-free")
PY
