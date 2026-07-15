#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-0819"
lean=$(cd "$root/Formalizations/Lean" && lake env which lean)
lean_path=$(cd "$root/Formalizations/Lean" && lake env printenv LEAN_PATH)
tmp=$(mktemp -d "$root/.m0819-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

LEAN_PATH="$lean_path" "$lean" --trust=0 -R "$here" -o "$tmp/Statement.olean" \
  "$here/Statement.lean" > "$tmp/statement.out"
LEAN_PATH="$lean_path" "$lean" --trust=0 -R "$here" -o "$tmp/FiniteDilworth.olean" \
  "$here/FiniteDilworth.lean" > "$tmp/finite.out"
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -R "$here" -o "$tmp/Proof.olean" \
  "$here/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/finite.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

finite = Path(sys.argv[1]).read_text(encoding="utf-8")
proof = Path(sys.argv[2]).read_text(encoding="utf-8")

expected = {
    "minAntichainPartition_eq_chainHeight":
        {"propext", "Classical.choice", "Quot.sound"},
    "minChainPartition_eq_antichainWidth":
        {"propext", "Classical.choice", "Quot.sound"},
    "Stage1Instances.THM_M_0819_Proof.dilworthPrimary":
        {"propext", "Classical.choice", "Quot.sound"},
}
for declaration, allowed in expected.items():
    output = proof if "dilworthPrimary" in declaration else finite
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",")}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"

assert "Declarations are sorry-free!" in proof
assert "sorryAx" not in finite + proof
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/FiniteDilworth.olean"
test -s "$tmp/Proof.olean"
echo "PASS THM-M-0819 isolated exact-root proof elaboration"
