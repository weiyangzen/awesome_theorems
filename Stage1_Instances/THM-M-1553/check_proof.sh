#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1553"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,ProofLemmas,Proof}.lean "$tmp/"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" -o Statement.olean Statement.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" -o ObligationTree.olean ObligationTree.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" -o ProofLemmas.olean ProofLemmas.lean >/dev/null
LEAN_PATH=".:$lean_path" "$lean_bin" Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1553.logarithmic_bilinear_identity",
    "Stage1Instances.THM_M_1553.logDerivativeBridge",
    "Stage1Instances.THM_M_1553.hirotaKdVTarget_proof",
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

python3 "$target/check_proof.py"
printf '%s\n' 'PASS THM-M-1553 proof replay: exact Hirota-to-KdV target checked'
