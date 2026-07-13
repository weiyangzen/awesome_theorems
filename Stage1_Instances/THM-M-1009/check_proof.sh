#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1009"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-1009-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

toolchain="$(cat "$lean_root/lean-toolchain")"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

cd "$lean_root"
LEAN_PATH="$lean_path" ELAN_TOOLCHAIN="$toolchain" \
  lake env lean -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean" >/dev/null
LEAN_PATH="$tmp:$lean_path" ELAN_TOOLCHAIN="$toolchain" \
  lake env lean -R "$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" >/dev/null
LEAN_PATH="$tmp:$lean_path" ELAN_TOOLCHAIN="$toolchain" \
  lake env lean -R "$tmp" "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in (
    "Stage1Instances.THM_M_1009.erdosRenyiLowerBoundTarget",
    "Stage1Instances.THM_M_1009.erdosRenyiObligationRoot_via_frozen_composition",
):
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axioms for {declaration}: {actual}"
assert "sorryAx" not in output
assert "error:" not in output
print("PASS THM-M-1009 Lean proof: exact root and frozen composition elaborated")
PY
