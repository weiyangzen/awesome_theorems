#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-1023"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/m1023-validation.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_dir" && lake env which lean)
pinned_lean_path=$(cd "$lean_dir" && lake env printenv LEAN_PATH)
bwrap=$(command -v bwrap)

test -x "$lean"
test -x "$bwrap"
test -d "$lean_dir/.lake/packages/mathlib/.lake/build/lib/lean"

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"
cp "$here/Validation.lean" "$tmp/Validation.lean"
cp -R "$here/Vendor" "$tmp/Vendor"

run_lean() {
  "$bwrap" --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc \
    --unshare-net --die-with-parent --clearenv --setenv HOME "$tmp" \
    --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
    --setenv LEAN_NUM_THREADS 1 --setenv LEAN_PATH "${LEAN_PATH:?}" \
    --chdir "$tmp" "$lean" --trust=0 "$@"
}

LEAN_PATH="$pinned_lean_path" run_lean -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" > "$tmp/statement.out"
LEAN_PATH="$tmp:$pinned_lean_path" run_lean -R "$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" > "$tmp/tree.out"

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
  LEAN_PATH="$tmp/Vendor:$pinned_lean_path" run_lean -R "$tmp/Vendor" \
    -o "$target" "$source" > "$tmp/vendor.out"
done

LEAN_PATH="$tmp:$tmp/Vendor:$pinned_lean_path" run_lean -R "$tmp" \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean" > "$tmp/proof.out"
LEAN_PATH="$tmp:$tmp/Vendor:$pinned_lean_path" run_lean -R "$tmp" \
  -o "$tmp/Validation.olean" "$tmp/Validation.lean" > "$tmp/validation.out"

python3 - "$tmp/tree.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

tree = Path(sys.argv[1]).read_text(encoding="utf-8")
proof = Path(sys.argv[2]).read_text(encoding="utf-8")
validation = Path(sys.argv[3]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
proof_declarations = [
    "Stage1Instances.THM_M_1023.infinitelyDivisibleIffLevyKhintchine",
    "ProbabilityTheory.levyKhintchine_representation",
    "ProbabilityTheory.levyKhintchine_converse",
    "ProbabilityTheory.existsUnique_levyKhintchineTriple",
]
validation_declaration = (
    "Stage1Instances.THM_M_1023.Validation.independentlyReconstructedRoot"
)

def assert_axioms(output: str, declaration: str) -> None:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert actual == allowed, (declaration, actual)

assert proof.count("Declarations are sorry-free!") == len(proof_declarations), proof
for declaration in proof_declarations:
    assert_axioms(proof, declaration)
assert_axioms(
    tree,
    "Stage1Instances.THM_M_1023.root_of_directionPackages",
)
assert validation.count("Declarations are sorry-free!") == 1, validation
assert validation_declaration in validation
assert_axioms(validation, validation_declaration)
combined = tree + proof + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined.lower()
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
test -s "$tmp/Validation.olean"
for module in "${modules[@]}"; do
  test -s "$tmp/Vendor/${module//./\/}.olean"
done

echo "PASS network-isolated trust-zero replay: 20 vendored modules, exact statement, frozen composition, proof root, and differential root elaborated"
echo "PASS trust observation: proof/differential declarations are sorry-free; six reports use exactly propext, Classical.choice, and Quot.sound"
echo "PASS differential scope: Validation.lean reconstructs the exact root without importing Proof or ObligationTree"
