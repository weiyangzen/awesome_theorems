#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1246"
lean_root="$repo_root/Formalizations/Lean"
lean_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
tmp="$(mktemp -d "$repo_root/.m1246-proof.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,RegularizedIBP,SharpEstimate,HardyLimit,Proof}.lean "$tmp/"

base_lean_path="$(find "$lean_root/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | paste -sd:):$(readlink -f "$lean_root/.lake")/build/lib/lean"

LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" timeout 600s \
  "$lean_bin" --trust=0 -t0 -o "$tmp/Statement.olean" "$tmp/Statement.lean" >/dev/null

for module in ObligationTree RegularizedIBP SharpEstimate HardyLimit; do
  LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout 600s \
    "$lean_bin" --trust=0 -t0 -o "$tmp/$module.olean" "$tmp/$module.lean" >/dev/null
done

LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout 600s \
  "$lean_bin" --trust=0 -t0 "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1246.Proof.hardyTerminal",
    "Stage1Instances.THM_M_1246.Proof.hardyInequality",
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
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-1246 raw kernel proof and axiom reports")
PY
