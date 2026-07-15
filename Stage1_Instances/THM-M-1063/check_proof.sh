#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=Asia/Shanghai
export LEAN_NUM_THREADS=1

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
LEAN_PROJECT="$ROOT/Formalizations/Lean"
TARGET="$ROOT/Stage1_Instances/THM-M-1063"
TMP=$(mktemp -d "${TMPDIR:-/tmp}/thm-m-1063-proof.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

replay_mode=lake_env
if LEAN_BIN=$(cd "$LEAN_PROJECT" && timeout 30 env -u LEAN_PATH lake env which lean 2>"$TMP/lake.err") &&
    LEAN_PATH_PINNED=$(cd "$LEAN_PROJECT" && timeout 30 env -u LEAN_PATH lake env printenv LEAN_PATH 2>>"$TMP/lake.err"); then
  :
else
  replay_mode=direct_pinned_fallback
  TOOLCHAIN=$(tr -d '\r\n' < "$LEAN_PROJECT/lean-toolchain")
  TOOLCHAIN_DIR=$(printf '%s' "$TOOLCHAIN" | sed 's#/#--#g; s#:#---#g')
  LEAN_BIN="$HOME/.elan/toolchains/$TOOLCHAIN_DIR/bin/lean"
  LEAN_PATH_PINNED=$(find -L "$LEAN_PROJECT/.lake/packages" -maxdepth 6 -type d \
    -path '*/.lake/build/lib/lean' -print | sort | paste -sd: -)
  LEAN_PATH_PINNED="$LEAN_PATH_PINNED:$LEAN_PROJECT/.lake/build/lib/lean"
  printf '%s\n' \
    'NOTICE: top-level lake env unavailable; using existing pinned compiled artifacts read-only' \
    "$(tr '\n' ' ' < "$TMP/lake.err")"
fi

test -x "$LEAN_BIN"
test -n "$LEAN_PATH_PINNED"
version=$($LEAN_BIN --version)
case "$version" in
  *'version 4.29.0'*'commit 98dc76e3c0a9b856c9b98726b713fb04fab16740'*) ;;
  *) printf 'FAIL: unexpected Lean executable: %s\n' "$version" >&2; exit 1 ;;
esac

LEAN_PATH="$LEAN_PATH_PINNED" timeout --foreground --kill-after=10s 300s \
  "$LEAN_BIN" --trust=0 -t0 "$TARGET/Proof.lean" >"$TMP/proof.out" 2>&1
cat "$TMP/proof.out"

python3 - "$TMP/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "AwesomeTheorems.Stage1.THM_M_1063.Proof.standardizedIncrement_package",
    "AwesomeTheorems.Stage1.THM_M_1063.Proof.scalarPartialSums_tendstoInDistribution",
)
allowed = ["propext", "Classical.choice", "Quot.sound"]
reports = re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]", output, re.DOTALL)
by_name = {name: [part.strip() for part in raw.split(",") if part.strip()]
           for name, raw in reports}
assert set(by_name) == set(declarations), (
    f"axiom-report coverage mismatch: expected={declarations}, actual={tuple(by_name)}"
)
for declaration in declarations:
    assert by_name[declaration] == allowed, (
        f"unexpected axiom closure for {declaration}: {by_name[declaration]}"
    )
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert not re.search(r"(^|\n).*error(?:\([^)]*\))?:", output)
print("PASS THM-M-1063 trust-zero replay: two partial proof bodies checked")
PY

printf 'replay mode: %s\n' "$replay_mode"
printf '%s\n' \
  'closed frozen obligations: none; root remains open M4' \
  'theorem_complete=false; accepted state unchanged'
