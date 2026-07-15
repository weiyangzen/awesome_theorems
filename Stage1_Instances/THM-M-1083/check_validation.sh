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
tmp="$(mktemp -d /tmp/stage1-m1083-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

lean_bin="$(cd "$lean_root" && lake env which lean)"
base_lean_path="$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)"
lean_path="$tmp:$repo_root:$base_lean_path"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --setenv LEAN_NUM_THREADS 1 --setenv LEAN_PATH "$lean_path"
)

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
  "${base[@]}" "$lean_bin" --trust=0 -t0 -R "$repo_root" \
    -o "$tmp/$relative.olean" "$vendor/$module" >/dev/null
done

mkdir -p "$tmp/Stage1_Instances/THM-M-1083"
"${base[@]}" "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  -o "$tmp/Stage1_Instances/THM-M-1083/Statement.olean" "$target/Statement.lean" \
  > "$tmp/statement.out"
"${base[@]}" "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  -o "$tmp/Stage1_Instances/THM-M-1083/ObligationTree.olean" "$target/ObligationTree.lean" \
  > "$tmp/obligation.out"
"${base[@]}" "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  -o "$tmp/Stage1_Instances/THM-M-1083/Proof.olean" "$target/Proof.lean" \
  > "$tmp/proof.out"
"${base[@]}" "$lean_bin" --trust=0 -t0 -R "$repo_root" \
  "$target/Validation.lean" > "$tmp/validation.out"

python3 - "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

proof_output = Path(sys.argv[1]).read_text(encoding="utf-8")
validation_output = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}


def observed_axioms(output: str, declaration: str) -> set[str]:
    if f"'{declaration}' does not depend on any axioms" in output:
        return set()
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


proof_declarations = (
    "Stage1Instances.THM_M_1083.Proof.timeInterval_hasBoundedCoveringNumber",
    "Stage1Instances.THM_M_1083.Proof.isKolmogorovProcess_of_increment",
    "Stage1Instances.THM_M_1083.Proof.kolmogorovContinuity",
    "Stage1Instances.THM_M_1083.Proof.canonicalProof",
)
for declaration in proof_declarations:
    assert observed_axioms(proof_output, declaration) == allowed, declaration
    assert observed_axioms(validation_output, declaration) == allowed, declaration

assert observed_axioms(
    validation_output, "ProbabilityTheory.exists_modification_holder"
) == allowed
assert observed_axioms(
    validation_output,
    "Stage1Instances.THM_M_1083.ObligationTree.kolmogorovContinuity_of_engine",
) <= allowed
assert validation_output.count("Declarations are sorry-free!") == 1

combined = proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "contains sorry" not in combined
assert "error:" not in combined

print("PASS THM-M-1083 network-isolated narrow kernel replay")
print("PASS exact root, vendored terminal, bridges, and frozen composition trust probes")
print("PASS transitive sorry check and observed axiom boundary: propext, Classical.choice, Quot.sound")
PY
