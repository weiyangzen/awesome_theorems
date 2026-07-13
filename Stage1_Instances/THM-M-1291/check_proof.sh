#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-1291"
lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
tmp=$(mktemp -d "$root/.m1291-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

cp "$here/Statement.lean" "$tmp/Statement.lean"
lean_lib="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
lean_path=""
while IFS= read -r package; do
  package_lib="$root/Formalizations/Lean/.lake/packages/$package/.lake/build/lib/lean"
  if test -d "$package_lib"; then
    lean_path="${lean_path}${package_lib}:"
  fi
done < <(python3 - "$root/Formalizations/Lean/lake-manifest.json" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as stream:
    manifest = json.load(stream)
for package in manifest["packages"]:
    print(package["name"].strip("«»"))
PY
)
lean_path="${lean_path}${root}/Formalizations/Lean/.lake/build/lib/lean:${lean_lib}"

test -x "$lean"
test -d "$lean_lib"
test -d "$root/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean"

LEAN_PATH="$lean_path" "$lean" --trust=0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" > "$tmp/statement.out"
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -R "$root" -o "$tmp/Proof.olean" \
  "$here/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declaration = "Stage1Instances.THM_M_1291.brezisLiebTarget_proof"
match = re.search(
    re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
    output,
    re.DOTALL,
)
assert match, f"missing axiom report for {declaration}"
actual = {name.strip() for name in match.group(1).split(",")}
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/Proof.olean"
echo "PASS THM-M-1291 isolated proof elaboration"
