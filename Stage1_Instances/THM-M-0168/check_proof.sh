#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 300s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

export LC_ALL=C.UTF-8
export TZ=UTC
export LEAN_NUM_THREADS=1

root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$root/Stage1_Instances/THM-M-0168"
lean_root="$root/Formalizations/Lean"
mathlib="$lean_root/.lake/packages/mathlib"
tmp="$(mktemp -d /tmp/thm-m-0168-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

# Select Lean through the immutable mathlib Lake project.  The unrelated
# top-level flt-regular checkout has no valid HEAD in this worker cache.
lean_bin="$(cd "$mathlib" && timeout 60 lake env which lean)"
lean_path_parts=()
while IFS= read -r path; do
  lean_path_parts+=("$path")
done < <(find -L "$lean_root/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d ! -path '*/flt-regular/*' -print | sort)
lean_path_parts+=("$(dirname "$lean_bin")/../lib/lean")
base_lean_path=$(IFS=:; printf '%s' "${lean_path_parts[*]}")

test -x "$lean_bin"
test -n "$base_lean_path"
test "$(git -C "$mathlib" rev-parse HEAD)" = \
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

run_lean() {
  local import_path=$1
  shift
  (cd "$mathlib" && timeout 240 lake env env \
    LEAN_NUM_THREADS="$LEAN_NUM_THREADS" LEAN_PATH="$import_path" \
    "$lean_bin" --root="$tmp" --trust=0 -t0 "$@")
}

run_lean "$base_lean_path" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean" >"$tmp/statement.out"
run_lean "$base_lean_path" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean" >"$tmp/obligation.out"
run_lean "$tmp:$base_lean_path" -o "$tmp/Proof.olean" \
  "$tmp/Proof.lean" >"$tmp/proof.out"

python3 - "$tmp/obligation.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

allowed = {"propext", "Classical.choice", "Quot.sound"}
expected = {
    "Stage1Instances.THM_M_0168_Obligations.constantPartials_to_affine": allowed,
    "Stage1Instances.THM_M_0168_Obligations.constantPartialsToAffine_proof": allowed,
    "Stage1Instances.THM_M_0168_Obligations.bernstein_of_derivativeRigidity": allowed,
    "Stage1Instances.THM_M_0168_Obligations.canonicalTarget_iff_obligationTarget": allowed,
    "Stage1Instances.THM_M_0168_Obligations.canonical_bernstein_of_derivativeRigidity": allowed,
}
output = Path(sys.argv[2]).read_text(encoding="utf-8")
reports = dict(re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL))
for declaration, wanted in expected.items():
    assert declaration in reports, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in reports[declaration].split(",") if part.strip()}
    assert actual == wanted, f"unexpected axioms for {declaration}: {sorted(actual)}"
combined = Path(sys.argv[1]).read_text(encoding="utf-8") + output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
print("PASS THM-M-0168 isolated proof replay: affine integration and canonical conditional transport checked")
print("closed child: M0168-T-INTEGRATE; root remains open M2")
PY

for source in "$target"/{Statement,ObligationTree,Proof}.lean; do
  sed '/^[[:space:]]*\/\-/,/\-\/[[:space:]]*$/d; /^[[:space:]]*--/d' "$source"
done >"$tmp/owned-code.lean"
if rg -n --pcre2 \
    '\b(?:sorry|admit|sorryAx|implemented_by|native_decide|run_tac)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern)[[:space:]]' \
    "$tmp/owned-code.lean"; then
  printf 'proof replay failed: prohibited proof device\n' >&2
  exit 1
fi

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
cat "$tmp/obligation.out" "$tmp/proof.out"
