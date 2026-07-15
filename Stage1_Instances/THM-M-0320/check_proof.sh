#!/usr/bin/env bash
set -euo pipefail

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-0320"
brouwer="$root/Stage1_Instances/THM-M-0318/Vendor"
lean_dir="$root/Formalizations/Lean"
tmp=$(mktemp -d "$root/.m0320-proof.XXXXXX")
trap 'rm -rf "$tmp"' EXIT

# Resolve the pinned toolchain through `lake env`. If an unrelated dependency
# artifact is missing, Lake fails before launching the already installed
# toolchain; report that fail-closed rather than fetching or mutating `.lake`.
if ! lean=$(cd "$lean_dir" && lake env which lean); then
  echo "BLOCKED: lake env cannot resolve the pinned toolchain; .lake was not mutated" >&2
  exit 3
fi
if ! pinned_lean_path=$(cd "$lean_dir" && lake env printenv LEAN_PATH); then
  echo "BLOCKED: lake env cannot resolve LEAN_PATH; .lake was not mutated" >&2
  exit 3
fi

test -x "$lean"
test -d "$lean_dir/.lake/packages/mathlib/.lake/build/lib/lean"

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$here/GraphBridgeProof.lean" "$tmp/GraphBridgeProof.lean"
cp "$here/BrouwerSource.lean" "$tmp/BrouwerSource.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"
cp -R "$brouwer" "$tmp/BrouwerVendor"

env LEAN_NUM_THREADS=1 LEAN_PATH="$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" > "$tmp/statement.out"
env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" > "$tmp/obligation-tree.out"
env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/GraphBridgeProof.olean" \
  "$tmp/GraphBridgeProof.lean" > "$tmp/graph-bridge.out"

for module in Gametheory.Scarf Gametheory.ScarfPath Gametheory.Brouwer; do
  source="$tmp/BrouwerVendor/${module//./\/}.lean"
  env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp/BrouwerVendor:$pinned_lean_path" \
    "$lean" --trust=0 -t0 -R "$tmp/BrouwerVendor" -o "${source%.lean}.olean" \
    "$source" > "$tmp/vendor.out"
done

env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$tmp/BrouwerVendor:$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/BrouwerSource.olean" \
  "$tmp/BrouwerSource.lean" > "$tmp/brouwer-source.out"
env LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$tmp/BrouwerVendor:$pinned_lean_path" \
  "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
match = re.search(
    r"'Stage1Instances\.THM_M_0320\.kakutaniFixedPoint' depends on axioms: \[(.*?)\]",
    output,
    re.DOTALL,
)
assert match, output
actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
assert actual == {"propext", "choice", "Quot.sound"}, actual
assert output.count("Declarations are sorry-free!") == 3, output
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output.lower()
PY

for output in Statement ObligationTree GraphBridgeProof BrouwerSource Proof; do
  test -s "$tmp/$output.olean"
done
for module in Gametheory/Scarf Gametheory/ScarfPath Gametheory/Brouwer; do
  test -s "$tmp/BrouwerVendor/$module.olean"
done

echo "PASS THM-M-0320 exact proof elaboration (MIT Brouwer source, --trust=0 -t0)"
