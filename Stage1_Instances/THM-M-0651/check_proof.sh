#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 360s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0651"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0651-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/ProofLemmas.lean" "$tmp/ProofLemmas.lean"

cd "$lean_root"
for module in Statement ObligationTree ProofLemmas; do
  LEAN_NUM_THREADS=1 lake env lean --trust=0 -t0 --root="$tmp" \
    -o "$tmp/$module.olean" "$tmp/$module.lean" >"$tmp/$module.out" 2>&1
  cat "$tmp/$module.out"
  test -s "$tmp/$module.olean"
done

python3 - "$tmp/ProofLemmas.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
namespace = "Stage1Instances.THM_M_0651.ProofLemmas."
classical = (
    "countable_symbols",
    "countable_finite_arity_syntax",
    "exists_surjective_formula_schedule",
    "countable_avoidance_requirements",
    "exists_surjective_avoidance_schedule",
    "exists_consistent_avoidance_extension",
)
axiom_free = (
    "zero_arity_formula_requirement_inhabited",
    "zero_arity_tuple_requirement_inhabited",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for name in classical:
    declaration = namespace + name
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {part.strip() for part in match.group(1).split(",") if part.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
for name in axiom_free:
    expected = f"'{namespace}{name}' does not depend on any axioms"
    assert expected in output, f"missing axiom-free report for {name}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output.lower()
print("PASS THM-M-0651 isolated trust-zero replay: eight partial proof bodies checked")
PY

sha256sum "$tmp/Statement.olean" "$tmp/ObligationTree.olean" "$tmp/ProofLemmas.olean"
