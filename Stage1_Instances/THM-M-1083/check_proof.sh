#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 1800s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1083"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1083-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
base_lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"
export LEAN_PATH="$tmp:$repo_root:$base_lean_path"
export LEAN_NUM_THREADS=1

modules=(
  Auxiliary/Algebra.lean
  Auxiliary/ENNReal.lean
  Auxiliary/FiniteInf.lean
  Auxiliary/MeanInequalities.lean
  Auxiliary/Metric.lean
  Auxiliary/MeasureTheory.lean
  Auxiliary/Nat.lean
  Auxiliary/Topology.lean
  Continuity/Chaining.lean
  Continuity/CoveringNumber.lean
  Continuity/HasBoundedInternalCoveringNumber.lean
  Continuity/IsKolmogorovProcess.lean
  Continuity/KolmogorovChentsovInequality.lean
  Gaussian/StochasticProcesses.lean
  Continuity/KolmogorovChentsov.lean
)
vendor="$target/Vendor/BrownianMotion"
for module in "${modules[@]}"; do
  relative="Stage1_Instances/THM-M-1083/Vendor/BrownianMotion/${module%.lean}"
  mkdir -p "$tmp/$(dirname "$relative")"
  printf 'checking vendor module %s\n' "$module"
  "$lean_bin" --trust=0 -t0 -R "$repo_root" -o "$tmp/$relative.olean" "$vendor/$module"
done

mkdir -p "$tmp/Stage1_Instances/THM-M-1083"
"$lean_bin" --trust=0 -t0 -R "$repo_root" \
  -o "$tmp/Stage1_Instances/THM-M-1083/Statement.olean" "$target/Statement.lean" \
  > "$tmp/statement.out"
"$lean_bin" --trust=0 -t0 -R "$repo_root" "$target/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "Stage1Instances.THM_M_1083.Proof.timeInterval_hasBoundedCoveringNumber",
    "Stage1Instances.THM_M_1083.Proof.isKolmogorovProcess_of_increment",
    "Stage1Instances.THM_M_1083.Proof.kolmogorovContinuity",
    "Stage1Instances.THM_M_1083.Proof.canonicalProof",
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
print("PASS THM-M-1083 exact root and complete vendored source closure")
print("axiom closure: propext, Classical.choice, Quot.sound")
PY
