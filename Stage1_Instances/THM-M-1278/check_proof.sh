#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1278-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
paths=()
for package in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible checkdecls mathlib; do
  path="$lean_root/.lake/packages/$package/.lake/build/lib/lean"
  [[ -d "$path" ]] && paths+=("$path")
done
paths+=("$lean_root/.lake/build/lib/lean")
paths+=("$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
base_path=$(IFS=:; printf '%s' "${paths[*]}")

cp "$here/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"

cd "$tmp"
LEAN_NUM_THREADS=1 LEAN_PATH="$base_path" \
  timeout 300 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean \
  >obligation-tree.out
LEAN_NUM_THREADS=1 LEAN_PATH=".:$base_path" \
  timeout 300 "$lean" --trust=0 -t0 Proof.lean | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1278_Obligations.exists_subtract_mean",
    "Stage1Instances.THM_M_1278_Obligations.dirichletEnergy_subtractMean",
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
assert "error:" not in output
print("PASS THM-M-1278 isolated Lean replay: two local proof declarations checked")
PY
