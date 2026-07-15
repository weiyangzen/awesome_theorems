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

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0349"
lean_root="$repo_root/Formalizations/Lean"
canonical_lake="$(readlink -f "$lean_root/.lake")"
mathlib="$canonical_lake/packages/mathlib"
tmp="$(mktemp -d /tmp/stage1-m0349-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

# The top-level Lake project is temporarily obstructed by an unrelated empty
# flt-regular checkout.  Resolve the pinned executable through mathlib's healthy
# Lake project, then use only the canonical prebuilt dependency directories.
lean_path="$(find "$canonical_lake/packages" -path '*/.lake/build/lib/lean' \
  -type d -printf '%p:' | sort)${canonical_lake}/build/lib/lean:${HOME}/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"

cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"

ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  lake -d "$mathlib" env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean" > "$tmp/statement.out"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  lake -d "$mathlib" env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0349.fourierCoeff_conjugateMode",
    "Stage1Instances.THM_M_0349.conjugateMultiplier_zero",
    "Stage1Instances.THM_M_0349.conjugate_l2_bound",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output.lower()
print("PASS THM-M-0349 isolated Lean replay: concrete L2 candidate checked")
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/Proof.olean"
