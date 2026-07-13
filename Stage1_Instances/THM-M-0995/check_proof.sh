#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEAN_ROOT="$(cd "$HERE/../../Formalizations/Lean" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

BASE_LEAN_PATH="$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)"
LEAN_BIN="$(cd "$LEAN_ROOT" && lake env which lean)"
export ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0

cd "$HERE"
LEAN_PATH="$BASE_LEAN_PATH" "$LEAN_BIN" -o "$TMP/Statement.olean" Statement.lean >"$TMP/statement.log" 2>&1
LEAN_PATH="$TMP:$BASE_LEAN_PATH" "$LEAN_BIN" -o "$TMP/ObligationTree.olean" ObligationTree.lean >"$TMP/obligation.log" 2>&1
LEAN_PATH="$TMP:$BASE_LEAN_PATH" "$LEAN_BIN" Proof.lean >"$TMP/proof.log" 2>&1

cat "$TMP/statement.log" "$TMP/obligation.log" "$TMP/proof.log"

python3 - "$TMP/obligation.log" "$TMP/proof.log" <<'PY'
import re
import sys
from pathlib import Path

allowed = {"propext", "Classical.choice", "Quot.sound"}
reports = 0
for name in sys.argv[1:]:
    text = Path(name).read_text()
    assert "sorryAx" not in text, f"unexpected sorryAx in {name}"
    blocks = re.findall(r"depends on axioms:\s*\[([^]]*)\]", text, flags=re.S)
    reports += len(blocks)
    for block in blocks:
        observed = {part.strip() for part in block.split(",") if part.strip()}
        assert observed <= allowed, f"unexpected axioms in {name}: {sorted(observed - allowed)}"
assert reports >= 5, f"expected axiom reports, observed {reports}"
print(f"PASS axiom whitelist: {reports} reports, allowed={sorted(allowed)}")
PY

python3 check_proof_hygiene.py
