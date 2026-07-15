#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=Asia/Shanghai
export LEAN_NUM_THREADS=1

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LEAN_PROJECT="$ROOT/Formalizations/Lean"
TARGET="$ROOT/Stage1_Instances/THM-M-0510"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-0510-proof.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

TOOLCHAIN=$(tr -d '\r\n' < "$LEAN_PROJECT/lean-toolchain")
TOOLCHAIN_DIR=$(printf '%s' "$TOOLCHAIN" | sed 's#/#--#g; s#:#---#g')
LEAN_BIN="$HOME/.elan/toolchains/$TOOLCHAIN_DIR/bin/lean"
LEAN_PATH_PINNED=$(find -L "$LEAN_PROJECT/.lake/packages" -maxdepth 7 -type d \
  -path '*/.lake/build/lib/lean' -print | sort | paste -sd: -)
LEAN_PATH_PINNED="$LEAN_PATH_PINNED:$LEAN_PROJECT/.lake/build/lib/lean"

test -x "$LEAN_BIN"
test -n "$LEAN_PATH_PINNED"
version=$($LEAN_BIN --version)
case "$version" in
  *'version 4.29.0'*'commit 98dc76e3c0a9b856c9b98726b713fb04fab16740'*) ;;
  *) printf 'FAIL: unexpected Lean executable: %s\n' "$version" >&2; exit 1 ;;
esac

cp "$TARGET/Statement.lean" "$TARGET/Proof.lean" "$TMP/"

LEAN_PATH="$LEAN_PATH_PINNED" timeout --foreground --kill-after=10s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" "$TMP/Statement.lean" \
  >"$TMP/statement.out" 2>&1 || {
    cat "$TMP/statement.out"
    exit 1
  }
LEAN_PATH="$TMP:$LEAN_PATH_PINNED" timeout --foreground --kill-after=10s 300s \
  "$LEAN_BIN" --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean" >"$TMP/proof.out" 2>&1 || {
    cat "$TMP/proof.out"
    exit 1
  }
cat "$TMP/proof.out"

python3 - "$TMP/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_0510.coeff_ordinaryPartitionSeries",
    "Stage1Instances.THM_M_0510.geometricFactor_mul_oneSub",
    "Stage1Instances.THM_M_0510.hasProd_ordinaryPartitionSeries_geometric",
    "Stage1Instances.THM_M_0510.ordinaryPartitionSeries_eq_geometricProduct",
    "Stage1Instances.THM_M_0510.ordinaryPartitionSeries_mul_eulerProduct",
)
allowed = ["propext", "Classical.choice", "Quot.sound"]
reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
by_name = {
    name: [part.strip() for part in raw.split(",") if part.strip()]
    for name, raw in reports
}
assert set(by_name) == set(declarations), (declarations, tuple(by_name))
for declaration in declarations:
    assert by_name[declaration] == allowed, (declaration, by_name[declaration])
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", output)
print("PASS THM-M-0510 trust-zero replay: ordinary partition Euler product checked")
PY

printf '%s\n' \
  'provisionally closed obligation: M0510-N-EULER-PRODUCT' \
  'first remaining machine gate: M0510-N-COEFFICIENT' \
  'root remains open M3; theorem_complete=false'
