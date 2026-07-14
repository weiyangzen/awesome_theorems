#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-1023"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d "$root/.m1023-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_dir" && lake env which lean)
pinned_lean_path=$(cd "$lean_dir" && lake env printenv LEAN_PATH)

test -x "$lean"
test -d "$root/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean"

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"
cp -R "$here/Vendor" "$tmp/Vendor"

LEAN_PATH="$pinned_lean_path" "$lean" --trust=0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" > "$tmp/statement.out"

mapfile -t modules < <(python3 - "$here/vendor-manifest.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    manifest = json.load(stream)
for module in manifest["build_order"]:
    print(module)
PY
)

for module in "${modules[@]}"; do
  source="$tmp/Vendor/${module//./\/}.lean"
  target="${source%.lean}.olean"
  LEAN_PATH="$tmp/Vendor:$pinned_lean_path" "$lean" --trust=0 \
    -R "$tmp/Vendor" -o "$target" "$source" > "$tmp/vendor.out"
done

LEAN_PATH="$tmp:$tmp/Vendor:$pinned_lean_path" "$lean" --trust=0 \
  -R "$tmp" -o "$tmp/Proof.olean" "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = [
    "Stage1Instances.THM_M_1023.infinitelyDivisibleIffLevyKhintchine",
    "ProbabilityTheory.levyKhintchine_representation",
    "ProbabilityTheory.levyKhintchine_converse",
    "ProbabilityTheory.existsUnique_levyKhintchineTriple",
]
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert output.count("Declarations are sorry-free!") == len(declarations), output
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",")}
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
echo "PASS THM-M-1023 isolated proof elaboration (20 vendored modules, --trust=0)"
