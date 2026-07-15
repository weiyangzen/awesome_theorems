#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
repo=$(cd "$here/../.." && pwd)
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0419-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)

cp "$here/Statement.lean" "$tmp/Statement.lean"
cp "$here/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$here/Proof.lean" "$tmp/Proof.lean"

cd "$tmp"
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout 180 "$lean" --trust=0 -t0 \
  -o Statement.olean Statement.lean >statement.out
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 \
  -o ObligationTree.olean ObligationTree.lean >obligation-tree.out
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 \
  -o Proof.olean Proof.lean 2>&1 | tee proof.out

python3 - proof.out <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1.THM_M_0419.Proof.cyclotomicIdentify",
    "IsCyclotomicExtension.algEquiv",
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
print("PASS THM-M-0419 isolated Lean replay: M0419-C-CYCLOTOMIC-IDENTIFY checked")
PY
