#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-0508"
LEAN_ROOT="$ROOT/Formalizations/Lean"
MATHLIB_ROOT="$LEAN_ROOT/.lake/packages/mathlib"
TOOLCHAIN="leanprover/lean4:v4.29.0"
EXPECTED_AXIOMS="propext Classical.choice Quot.sound"

tmp=$(mktemp -d /tmp/stage1-m0508-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
direct="$tmp/direct"
lake_replay="$tmp/lake"
mkdir -p "$direct" "$lake_replay"

# Use only the existing compiled dependency artifacts. All newly generated
# objects stay in the temporary directory and are removed on exit.
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

IFS=: read -r -a base_paths <<< "$lean_path"
for module in Statement ObligationTree; do
  for base_path in "${base_paths[@]}"; do
    if [[ -e "$base_path/$module.olean" ]]; then
      echo "FAIL package object shadows local module: $base_path/$module.olean" >&2
      exit 1
    fi
  done
done

cd "$TARGET"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  elan run "$TOOLCHAIN" lean --trust=0 -t0 -o "$direct/Statement.olean" \
  Statement.lean >"$tmp/statement.out" 2>&1
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  elan run "$TOOLCHAIN" lean --trust=0 -t0 -o "$direct/ObligationTree.olean" \
  ObligationTree.lean >"$tmp/obligation.out" 2>&1
LEAN_PATH="$direct:$lean_path" LEAN_NUM_THREADS=1 \
  elan run "$TOOLCHAIN" lean --trust=0 -t0 Proof.lean \
  >"$tmp/proof.out" 2>&1

# Replay the same sources through `lake env lean` in pinned mathlib. Explicit
# roots and paths avoid creating artifacts or resolving new dependencies.
cd "$MATHLIB_ROOT"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$TARGET" \
  -o "$lake_replay/Statement.olean" "$TARGET/Statement.lean" \
  >"$tmp/lake-statement.out" 2>&1
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$TARGET" \
  -o "$lake_replay/ObligationTree.olean" "$TARGET/ObligationTree.lean" \
  >"$tmp/lake-obligation.out" 2>&1
LEAN_PATH="$lake_replay:$lean_path" LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 -t0 --root="$TARGET" "$TARGET/Proof.lean" \
  >"$tmp/lake-proof.out" 2>&1

cmp -s "$tmp/proof.out" "$tmp/lake-proof.out" || {
  echo "FAIL direct Lean and lake env lean proof outputs disagree" >&2
  diff -u "$tmp/proof.out" "$tmp/lake-proof.out" >&2 || true
  exit 1
}

python3 - "$tmp/proof.out" "$EXPECTED_AXIOMS" <<'PY'
import re
import sys

text = open(sys.argv[1], encoding="utf-8").read()
expected = set(sys.argv[2].split())
declarations = [
    "Stage1Instances.THM_M_0508.Proof."
    "vinogradovThreePrimesTarget_iff_eventualPositiveRepresentationCount",
    "Stage1Instances.THM_M_0508.Proof."
    "vinogradovThreePrimesTarget_of_eventualPositiveRepresentationCount",
]
for declaration in declarations:
    pattern = rf"'{re.escape(declaration)}' depends on axioms:\s*\[(.*?)\]"
    matches = re.findall(pattern, text, re.DOTALL)
    if len(matches) != 1:
        raise SystemExit(
            f"FAIL expected one complete axiom list for {declaration}, observed {len(matches)}"
        )
    actual = {name.strip() for name in matches[0].split(",") if name.strip()}
    if actual != expected:
        raise SystemExit(
            f"FAIL unexpected axioms for {declaration}: {sorted(actual)}"
        )
PY

[[ $(grep -cF "Declarations are sorry-free!" "$tmp/proof.out") -eq 2 ]] || {
  echo "FAIL missing exact sorry-free reports" >&2
  cat "$tmp/proof.out" >&2
  exit 1
}

if grep -Eq "error:|declaration uses 'sorry'" \
    "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" \
    "$tmp/lake-statement.out" "$tmp/lake-obligation.out" "$tmp/lake-proof.out"; then
  echo "FAIL Lean diagnostics" >&2
  cat "$tmp/statement.out" "$tmp/obligation.out" "$tmp/proof.out" >&2
  exit 1
fi

python3 "$TARGET/check_proof.py"
cat "$tmp/proof.out"
echo "PASS THM-M-0508 isolated canonical proof-interface replay"
