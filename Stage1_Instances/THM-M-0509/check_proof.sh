#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-0509"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB_ROOT="$LEAN_ROOT/.lake/packages/mathlib"
TOOLCHAIN="leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS="propext Classical.choice Quot.sound"

tmp=$(mktemp -d /tmp/stage1-m0509-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

# Lake cannot currently construct the root environment because the shared
# flt-regular checkout has no resolvable HEAD. Enumerate only the pre-existing
# compiled package directories and invoke the repository-pinned Lean version.
lean_path=""
while IFS= read -r path; do
  if [[ -d "$path" ]]; then
    if [[ -z "$lean_path" ]]; then
      lean_path="$path"
    else
      lean_path="$lean_path:$path"
    fi
  fi
done < <(find "$LEAN_ROOT/.lake/packages" -mindepth 1 -maxdepth 1 -type d \
  -printf '%p/.lake/build/lib/lean\n' | sort)

if [[ -z "$lean_path" ]]; then
  echo "FAIL no pre-existing compiled package artifacts" >&2
  exit 1
fi

cd "$TARGET"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  elan run "$TOOLCHAIN" lean --trust=0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/statement.out" 2>&1
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 \
  elan run "$TOOLCHAIN" lean --trust=0 Proof.lean >"$tmp/proof.out" 2>&1

# Also exercise `lake env lean` through the pinned mathlib package. Explicit
# LEAN_PATH and --root avoid root-project resolution of the unrelated broken
# flt-regular checkout while retaining the pinned Lake/Lean launcher.
cd "$MATHLIB_ROOT"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 --root="$TARGET" -o "$tmp/LakeStatement.olean" \
  "$TARGET/Statement.lean" >"$tmp/lake-statement.out" 2>&1
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 --root="$TARGET" "$TARGET/Proof.lean" \
  >"$tmp/lake-proof.out" 2>&1
cmp -s "$tmp/proof.out" "$tmp/lake-proof.out" || {
  echo "FAIL direct Lean and lake env lean outputs disagree" >&2
  diff -u "$tmp/proof.out" "$tmp/lake-proof.out" >&2 || true
  exit 1
}

for declaration in \
  Stage1Instances.THM_M_0509.Proof.isP2_iff_cardFactors_pos_le_two \
  Stage1Instances.THM_M_0509.Proof.representationCount_pos_iff \
  Stage1Instances.THM_M_0509.Proof.chenTheoremTarget_iff_eventualPositiveRepresentationCount; do
  grep -Fq "'$declaration' depends on axioms:" "$tmp/proof.out" || {
    echo "FAIL missing axiom report for $declaration" >&2
    cat "$tmp/proof.out" >&2
    exit 1
  }
done

for axiom in $EXPECTED_AXIOMS; do
  count=$(grep -oF "$axiom" "$tmp/proof.out" | wc -l)
  [[ "$count" -eq 3 ]] || {
    echo "FAIL expected three axiom reports containing $axiom, observed $count" >&2
    cat "$tmp/proof.out" >&2
    exit 1
  }
done

actual_axioms=$(sed -n '/depends on axioms:/,/]/p' "$tmp/proof.out" \
  | grep -oE 'propext|Classical\.choice|Quot\.sound|[A-Za-z_][A-Za-z0-9_.]*' \
  | grep -vE '^(depends|on|axioms|Stage1Instances\..*)$' \
  | sort -u | paste -sd' ' -)
expected_axioms=$(printf '%s\n' $EXPECTED_AXIOMS | sort -u | paste -sd' ' -)
[[ "$actual_axioms" == "$expected_axioms" ]] || {
  echo "FAIL unexpected axiom union: $actual_axioms" >&2
  exit 1
}

[[ $(grep -cF "Declarations are sorry-free!" "$tmp/proof.out") -eq 3 ]] || {
  echo "FAIL missing exact sorry-free reports" >&2
  cat "$tmp/proof.out" >&2
  exit 1
}

if grep -Eq "error:|declaration uses 'sorry'" \
    "$tmp/statement.out" "$tmp/proof.out" \
    "$tmp/lake-statement.out" "$tmp/lake-proof.out"; then
  echo "FAIL Lean diagnostics" >&2
  cat "$tmp/statement.out" "$tmp/proof.out" >&2
  exit 1
fi

python3 "$TARGET/check_proof.py"
cat "$tmp/proof.out"
echo "PASS THM-M-0509 isolated proof replay"
