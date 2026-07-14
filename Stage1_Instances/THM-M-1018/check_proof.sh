#!/usr/bin/env bash
set -euo pipefail

root=$(cd "$(dirname "$0")/../.." && pwd)
target="$root/Stage1_Instances/THM-M-1018"
lean_root="$root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1018-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)

cp "$target/Statement.lean" "$target/Proof.lean" "$tmp/"
cd "$tmp"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 --root="$tmp" -o Statement.olean Statement.lean \
  > statement.out
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 --root="$tmp" -o Proof.olean Proof.lean \
  | tee proof.out

python3 - proof.out <<'PY'
import pathlib
import sys

text = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
names = (
    "frontier_Ioc_null",
    "tendsto_Ioc_mass_of_tendsto",
    "measureReal_Icc_eq_Ioc",
    "measureReal_Ioo_eq_Ioc",
    "interval_mass_of_weak_limit",
)
assert text.count("depends on axioms:") == len(names), text
assert all(name in text for name in names), text
assert "sorryAx" not in text, text
for axiom in ("propext", "Classical.choice", "Quot.sound"):
    assert text.count(axiom) == len(names), text
print("PASS THM-M-1018 partial proof replay: 5 declarations, trust zero")
PY

