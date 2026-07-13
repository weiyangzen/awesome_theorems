#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0626"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" "$lean_bin" -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" "$lean_bin" Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "IsPreconnected.image",
    "IsConnected.image",
    "Stage1Instances.THM_M_0626.Proof.relativePreimages",
    "Stage1Instances.THM_M_0626.Proof.imageCoverPullback",
    "Stage1Instances.THM_M_0626.Proof.imageHitPullback",
    "Stage1Instances.THM_M_0626.Proof.sourceIntersection",
    "Stage1Instances.THM_M_0626.Proof.intersectionPushforward",
    "Stage1Instances.THM_M_0626.Proof.separationEngine",
    "Stage1Instances.THM_M_0626.Proof.imagePreconnected",
    "Stage1Instances.THM_M_0626.Proof.imageNonempty",
    "Stage1Instances.THM_M_0626.Proof.localConnectedImage_components",
    "Stage1Instances.THM_M_0626.Proof.localConnectedImage_mathlib",
    "Stage1Instances.THM_M_0626.Proof.connectedImage",
    "Stage1Instances.THM_M_0626.Proof.connectedImage_via_components",
    "Stage1Instances.THM_M_0626.Proof.connectedImage_via_exactAssembly",
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
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "error:" not in output
PY
