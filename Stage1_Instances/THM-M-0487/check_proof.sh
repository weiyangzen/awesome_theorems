#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-0487"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB_ROOT="$LEAN_ROOT/.lake/packages/mathlib"
EXPECTED_AXIOMS="propext Classical.choice Quot.sound"

tmp=$(mktemp -d /tmp/stage1-m0487-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
if [[ ! -x "$lean" ]]; then
  echo "FAIL pinned Lean executable is unavailable at $lean" >&2
  exit 1
fi

# Enumerate only pre-existing pinned build artifacts. The Lake replay below
# remains the primary launcher check; this avoids repeated root resolution.
lean_path="$LEAN_ROOT/.lake/build/lib/lean"
while IFS= read -r path; do
  [[ -d "$path" ]] && lean_path="$lean_path:$path"
done < <(find "$LEAN_ROOT/.lake/packages" -mindepth 1 -maxdepth 1 -type d \
  -printf '%p/.lake/build/lib/lean\n' | sort)
if [[ -z "$lean_path" ]]; then
  echo "FAIL lake env returned an empty LEAN_PATH" >&2
  exit 1
fi

cd "$TARGET"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 180s \
  "$lean" --trust=0 -o "$tmp/Statement.olean" Statement.lean \
  >"$tmp/statement.out" 2>&1
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 180s \
  "$lean" --trust=0 -o "$tmp/ObligationTree.olean" ObligationTree.lean \
  >"$tmp/obligation.out" 2>&1
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 180s \
  "$lean" --trust=0 Proof.lean >"$tmp/proof.out" 2>&1

# Repeat through the manifest-pinned Lake launcher without writing into `.lake`.
cd "$MATHLIB_ROOT"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 180s \
  lake env lean --trust=0 --root="$TARGET" -o "$tmp/LakeStatement.olean" \
  "$TARGET/Statement.lean" >"$tmp/lake-statement.out" 2>&1
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 180s \
  lake env lean --trust=0 --root="$TARGET" -o "$tmp/LakeObligationTree.olean" \
  "$TARGET/ObligationTree.lean" >"$tmp/lake-obligation.out" 2>&1
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 180s \
  lake env lean --trust=0 --root="$TARGET" "$TARGET/Proof.lean" \
  >"$tmp/lake-proof.out" 2>&1
sed "s|$TARGET/Proof.lean|Proof.lean|g" "$tmp/lake-proof.out" >"$tmp/lake-proof-normalized.out"
cmp -s "$tmp/proof.out" "$tmp/lake-proof-normalized.out" || {
  echo "FAIL normalized direct pinned Lean and lake env lean outputs disagree" >&2
  diff -u "$tmp/proof.out" "$tmp/lake-proof-normalized.out" >&2 || true
  exit 1
}

for declaration in \
  Stage1Instances.THM_M_0487.Proof.representationCount_pos_iff \
  Stage1Instances.THM_M_0487.Proof.weakGoldbachTarget_iff_positiveRepresentationCountTarget; do
  grep -Fq "'$declaration' depends on axioms:" "$tmp/proof.out" || {
    echo "FAIL missing axiom report for $declaration" >&2
    cat "$tmp/proof.out" >&2
    exit 1
  }
done

for axiom in $EXPECTED_AXIOMS; do
  count=$(grep -oF "$axiom" "$tmp/proof.out" | wc -l)
  [[ "$count" -eq 2 ]] || {
    echo "FAIL expected two axiom reports containing $axiom, observed $count" >&2
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

[[ $(grep -cF "Declarations are sorry-free!" "$tmp/proof.out") -eq 2 ]] || {
  echo "FAIL missing exact sorry-free reports" >&2
  cat "$tmp/proof.out" >&2
  exit 1
}

if grep -Eq "error:|declaration uses 'sorry'" \
    "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
    "$tmp/lake-statement.out" "$tmp/lake-obligation.out" "$tmp/lake-proof.out"; then
  echo "FAIL Lean diagnostics" >&2
  cat "$tmp/statement.out" "$tmp/proof.out" >&2
  exit 1
fi

if [[ -f "$TARGET/check_proof.py" ]]; then
  python3 -B "$TARGET/check_proof.py"
fi
cat "$tmp/proof.out"
echo "PASS THM-M-0487 isolated partial proof replay"
