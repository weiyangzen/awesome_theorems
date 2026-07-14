#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0526"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0526-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

tmp_target="$tmp/Stage1_Instances/THM-M-0526"
mkdir -p "$tmp_target"
cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp_target/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 240 "$lean_bin" --trust=0 -t0 \
  -R "$tmp" -o "$tmp_target/Statement.olean" "$tmp_target/Statement.lean" >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean_bin" --trust=0 -t0 \
  -R "$tmp" -o "$tmp_target/ObligationTree.olean" "$tmp_target/ObligationTree.lean" >/dev/null
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 240 "$lean_bin" --trust=0 -t0 \
  -R "$tmp" "$tmp_target/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0526.square_commutativity_proof",
    "Stage1Instances.THM_M_0526.square_package",
    "Stage1Instances.THM_M_0526.path_subdivision_of_two_open_cover",
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
    assert actual <= allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS: three THM-M-0526 local proof bodies elaborated with allowed axioms")
PY
