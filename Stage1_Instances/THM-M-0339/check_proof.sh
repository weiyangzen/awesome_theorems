#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/../.." && pwd)
here="$root/Stage1_Instances/THM-M-0339"
lean_root="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/stage1-m0339-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

toolchain=$(tr -d '\r\n' < "$lean_root/lean-toolchain")
toolchain_dir=$(printf '%s' "$toolchain" | sed 's#/#--#g; s#:#---#g')
lean="$HOME/.elan/toolchains/$toolchain_dir/bin/lean"
base_lean_path=$(find -L "$lean_root/.lake/packages" -path '*/.lake/build/lib/lean' \
  -type d -print | sort | paste -sd: -)

test -x "$lean"
test -n "$base_lean_path"
cp "$here"/{Statement,Proof}.lean "$tmp/"

LEAN_NUM_THREADS=1 LEAN_PATH="$base_lean_path" timeout 300 \
  "$lean" --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" timeout 300 \
  "$lean" --trust=0 -t0 --root="$tmp" "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1.THM_M_0339.Proof.one_part",
    "Stage1.THM_M_0339.Proof.zero_dimension",
    "Stage1.THM_M_0339.Proof.empty_family",
    "Stage1.THM_M_0339.Proof.enough_colors",
    "Stage1.THM_M_0339.Proof.constant_color_large_bound",
    "Stage1.THM_M_0339.Proof.delta_ge_one",
    "Stage1.THM_M_0339.Proof.zero_delta",
    "Stage1.THM_M_0339.Proof.mssPartitionStatement_of_hardRegimeEngine",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert actual == allowed, f"unexpected axioms for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
print("PASS THM-M-0339 isolated proof replay: seven elementary bodies and residual composition")
print("root remains conditional on HardRegimeEngine; theorem_complete=false")
PY

