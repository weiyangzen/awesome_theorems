#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0028"
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
expected = {
    "isNoetherianRing_iff_ideal_fg": {"propext", "Quot.sound"},
    "monotone_stabilizes_iff_noetherian": {
        "propext", "Classical.choice", "Quot.sound"
    },
    "Stage1Instances.THM_M_0028.Proof.finiteGenerationToNoetherian": {
        "propext", "Quot.sound"
    },
    "Stage1Instances.THM_M_0028.Proof.noetherianToChainStabilization": {
        "propext", "Classical.choice", "Quot.sound"
    },
    "Stage1Instances.THM_M_0028.Proof.idealAscendingChainTheorem_direct": {
        "propext", "Classical.choice", "Quot.sound"
    },
    "Stage1Instances.THM_M_0028.Proof.idealAscendingChainTheorem_via_frozen_composition": {
        "propext", "Classical.choice", "Quot.sound"
    },
}
for declaration, allowed in expected.items():
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == len(expected)
assert "sorryAx" not in output
PY
