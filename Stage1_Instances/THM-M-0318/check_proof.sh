#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-0318"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d "$root/.m0318-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_dir" && lake env which lean)
pinned_lean_path=$(cd "$lean_dir" && lake env printenv LEAN_PATH)

test -x "$lean"
test -d "$root/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean"

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"
cp -R "$here/Vendor" "$tmp/Vendor"

env LEAN_NUM_THREADS=1 LEAN_PATH="$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" > "$tmp/statement.out"
env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" > "$tmp/obligation-tree.out"

modules=(Gametheory.Scarf Gametheory.ScarfPath Gametheory.Brouwer)
for module in "${modules[@]}"; do
  source="$tmp/Vendor/${module//./\/}.lean"
  target="${source%.lean}.olean"
  env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp/Vendor:$pinned_lean_path" \
    "$lean" --trust=0 -t0 -R "$tmp/Vendor" -o "$target" "$source" \
    > "$tmp/vendor.out"
done

env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$tmp/Vendor:$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "IndexedLOrder.Scarf",
    "IndexedLOrder.GiComponentStructure_holds",
    "Brouwer",
    "Stage1Instances.THM_M_0318.exists_simplex_approximation",
    "Stage1Instances.THM_M_0318.hasApproximateFixedPoints",
    "Stage1Instances.THM_M_0318.approximationEngine",
    "Stage1Instances.THM_M_0318.compactLimitEngine",
    "Stage1Instances.THM_M_0318.exactSchauderTarget",
    "Stage1Instances.THM_M_0318.schauderFixedPoint",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert output.count("Declarations are sorry-free!") == len(declarations), output
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {
        name.strip() for name in match.group(1).split(",") if name.strip()
    }
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output.lower()
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
for module in "${modules[@]}"; do
  test -s "$tmp/Vendor/${module//./\/}.olean"
done
echo "PASS THM-M-0318 isolated proof elaboration (3 vendored modules, --trust=0 -t0)"
