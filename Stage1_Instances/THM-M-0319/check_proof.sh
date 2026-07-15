#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=UTC

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-0319"
lean_dir="$root/Formalizations/Lean"
mathlib_dir=$(readlink -f "$lean_dir/.lake")/packages/mathlib
tmp=$(mktemp -d "/tmp/m0319-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# The top-level Lake environment currently has an independently disclosed,
# incomplete flt-regular checkout. Querying mathlib only selects the pinned
# executable; compose imports from already materialized top-level artifacts.
lean=$(cd "$mathlib_dir" && timeout 60 lake env which lean)
lean_path_parts=()
while IFS= read -r path; do
  lean_path_parts+=("$path")
done < <(find -L "$(readlink -f "$lean_dir/.lake")/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | sort)
lean_path_parts+=("$(readlink -f "$lean_dir/.lake")/build/lib/lean")
lean_path_parts+=("$(dirname "$lean")/../lib/lean")
pinned_lean_path=$(IFS=:; printf '%s' "${lean_path_parts[*]}")

test -x "$lean"
test "$(git -C "$mathlib_dir" rev-parse HEAD)" = \
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"
test -d "$mathlib_dir/.lake/build/lib/lean"

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"
cp -R "$here/Vendor" "$tmp/Vendor"

env LEAN_NUM_THREADS=1 LEAN_PATH="$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" > "$tmp/statement.out"

modules=(Gametheory.Scarf Gametheory.ScarfPath Gametheory.Brouwer)
for module in "${modules[@]}"; do
  source="$tmp/Vendor/${module//./\/}.lean"
  target="${source%.lean}.olean"
  module_log="$tmp/${module//./-}.out"
  env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp/Vendor:$pinned_lean_path" \
    "$lean" --trust=0 -t0 -R "$tmp/Vendor" -o "$target" "$source" \
    > "$module_log"
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
    "Stage1Instances.THM_M_0319.exists_simplex_approximation",
    "Stage1Instances.THM_M_0319.hasApproximateFixedPoints",
    "Stage1Instances.THM_M_0319.exactFixedPoint",
    "Stage1Instances.THM_M_0319.brouwerFixedPoint",
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
test -s "$tmp/Proof.olean"
for module in "${modules[@]}"; do
  test -s "$tmp/Vendor/${module//./\/}.olean"
done
echo "PASS THM-M-0319 isolated proof elaboration (3 vendored modules, --trust=0 -t0)"
