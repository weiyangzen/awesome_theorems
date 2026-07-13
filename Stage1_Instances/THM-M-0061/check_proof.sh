#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0061"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0061-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_path="$(lake env printenv LEAN_PATH)"
lean_bin="$(lake env which lean)"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" -o Statement.olean Statement.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" Proof.lean | tee proof.out

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "fiberDecomposition",
    "fiberToLeftCoset",
    "leftCosetEquivalence",
    "sigmaProductEquivalence",
    "cosetProductEquivalence",
    "natCardProduct",
    "natCardCongruence",
    "cardProductIdentity",
    "pinnedCardProductIdentity",
    "arbitraryGroupDivisibility",
    "pinnedArbitraryGroupDivisibility",
    "finiteGroupDivisibility",
    "lagrangeDivisibility",
    "lagrangeDivisibility_mathlib",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
namespace = "Stage1Instances.THM_M_0061.Proof."
for short_name in declarations:
    declaration = namespace + short_name
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "error:" not in output
PY
