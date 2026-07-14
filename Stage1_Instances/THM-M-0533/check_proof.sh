#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0533"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0533-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean_bin" --trust=0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" "$lean_bin" --trust=0 Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declaration = "AwesomeTheorems.THM_M_0533.firstMap_comp_secondMap"
match = re.search(
    re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
    output,
    re.DOTALL,
)
assert match, f"missing axiom report for {declaration}"
actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
assert actual <= {"propext", "Classical.choice", "Quot.sound"}, actual
assert "sorryAx" not in output
assert "error:" not in output
PY

python3 "$target/check_proof.py"

printf '%s\n' \
  'PASS THM-M-0533 partial proof: firstMap_comp_secondMap checked' \
  'closed frozen obligations: none; root closure remains open (M3)'
