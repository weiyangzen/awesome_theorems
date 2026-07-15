#!/usr/bin/env bash
set -euo pipefail

script_path="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
if [[ "${1:-}" != "--bounded-inner" ]]; then
  if (( $# != 0 )); then
    printf 'usage: bash %s\n' "$0" >&2
    exit 2
  fi
  exec timeout --foreground --kill-after=10s 600s bash "$script_path" --bounded-inner
fi
if (( $# != 1 )); then
  printf 'invalid internal invocation\n' >&2
  exit 2
fi

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1065"
lean_root="$repo_root/Formalizations/Lean"
mathlib="$lean_root/.lake/packages/mathlib"
tmp="$(mktemp -d /tmp/stage1-m1065-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible; do
  test -d "$lean_root/.lake/packages/$package/.lake/build/lib/lean"
done
test -d "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean"
test "$(git -C "$mathlib" status --porcelain=v1 --untracked-files=no)" = ""

# The toolchain and LEAN_PATH are assembled only from already-present pinned artifacts. Lake project
# discovery is intentionally avoided because the root manifest's unrelated flt-regular dependency is
# not part of this target's imports and may be under concurrent scheduler maintenance.
toolchain_bin="$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/bin"
lean_bin="$toolchain_bin/lean"
lean_path=""
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  if [[ -n "$lean_path" ]]; then
    lean_path="$lean_path:"
  fi
  lean_path="$lean_path$lean_root/.lake/packages/$package/.lake/build/lib/lean"
done
lean_path="$lean_path:$lean_root/.lake/build/lib/lean:$toolchain_bin/../lib/lean"

for name in Statement.lean ObligationTree.lean Proof.lean AnchorAudit.lean Validation.lean; do
  cp "$target/$name" "$tmp/$name"
done
mkdir -p "$tmp/home"

base=(
  bwrap --clearenv --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent
  --setenv HOME "$tmp/home" --setenv PATH /usr/bin:/bin
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --setenv LEAN_NUM_THREADS 1 --setenv NO_COLOR 1
  --chdir "$tmp"
)

run_lean() {
  local source="$1"
  local active_path="$2"
  local log="$3"
  local output="${4:-}"
  local -a output_args=()
  if [[ -n "$output" ]]; then
    output_args=(-o "$output")
  fi
  "${base[@]}" --setenv LEAN_PATH "$active_path" \
    "$lean_bin" --trust=0 -t0 --root="$tmp" "${output_args[@]}" "$source" \
    >"$tmp/$log" 2>&1
}

run_lean Statement.lean "$lean_path" Statement.out "$tmp/Statement.olean"
run_lean ObligationTree.lean "$lean_path" ObligationTree.out "$tmp/ObligationTree.olean"
run_lean AnchorAudit.lean "$lean_path" AnchorAudit.out "$tmp/AnchorAudit.olean"
local_path="$tmp:$lean_path"
run_lean Proof.lean "$local_path" Proof.out "$tmp/Proof.olean"
run_lean Validation.lean "$local_path" Validation.out "$tmp/Validation.olean"

cat >"$tmp/StatementProbe.lean" <<'LEAN'
import Statement

#check Stage1Instances.THM_M_1065.KMTStrongApproximationTarget
#print sorries Stage1Instances.THM_M_1065.target_iff_expandedSourceShape
#print axioms Stage1Instances.THM_M_1065.target_iff_expandedSourceShape
#print sorries Stage1Instances.THM_M_1065.discrepancyEvent_one
#print axioms Stage1Instances.THM_M_1065.discrepancyEvent_one
LEAN

cat >"$tmp/CompositionProbe.lean" <<'LEAN'
import ObligationTree

#print sorries Stage1Instances.THM_M_1065.ObligationTree.kmtTarget_iff_couplingData
#print axioms Stage1Instances.THM_M_1065.ObligationTree.kmtTarget_iff_couplingData
LEAN

cat >"$tmp/ProofProbe.lean" <<'LEAN'
import Proof

#print sorries Stage1Instances.THM_M_1065.exists_commonIIDSequences
#print axioms Stage1Instances.THM_M_1065.exists_commonIIDSequences
#print sorries Stage1Instances.THM_M_1065.measurableSet_discrepancyEvent
#print axioms Stage1Instances.THM_M_1065.measurableSet_discrepancyEvent
LEAN

cat >"$tmp/AnchorProbe.lean" <<'LEAN'
import AnchorAudit

#print sorries Stage1Instances.THM_M_1065.AnchorAudit.noRetainedCandidateClaimsTerminalProof
#print axioms Stage1Instances.THM_M_1065.AnchorAudit.noRetainedCandidateClaimsTerminalProof
#print sorries Stage1Instances.THM_M_1065.AnchorAudit.anchorAuditPermitsTheoremCompletion_eq_false
#print axioms Stage1Instances.THM_M_1065.AnchorAudit.anchorAuditPermitsTheoremCompletion_eq_false
LEAN

run_lean StatementProbe.lean "$local_path" StatementProbe.out
run_lean CompositionProbe.lean "$local_path" CompositionProbe.out
run_lean ProofProbe.lean "$local_path" ProofProbe.out
run_lean AnchorProbe.lean "$local_path" AnchorProbe.out

for log in StatementProbe CompositionProbe ProofProbe AnchorProbe Validation; do
  printf '===== %s =====\n' "$log"
  cat "$tmp/$log.out"
done

python3 -I - "$tmp" <<'PY'
import re
import sys
from pathlib import Path

target = Path(sys.argv[1])
allowed = {"propext", "Classical.choice", "Quot.sound"}
groups = {
    "StatementProbe.out": (
        "Stage1Instances.THM_M_1065.target_iff_expandedSourceShape",
        "Stage1Instances.THM_M_1065.discrepancyEvent_one",
    ),
    "CompositionProbe.out": (
        "Stage1Instances.THM_M_1065.ObligationTree.kmtTarget_iff_couplingData",
    ),
    "ProofProbe.out": (
        "Stage1Instances.THM_M_1065.exists_commonIIDSequences",
        "Stage1Instances.THM_M_1065.measurableSet_discrepancyEvent",
    ),
    "AnchorProbe.out": (
        "Stage1Instances.THM_M_1065.AnchorAudit.noRetainedCandidateClaimsTerminalProof",
        "Stage1Instances.THM_M_1065.AnchorAudit.anchorAuditPermitsTheoremCompletion_eq_false",
    ),
    "Validation.out": (
        "Stage1Instances.THM_M_1065.Validation.independentlyReconstructedTargetExpansion",
        "Stage1Instances.THM_M_1065.Validation.independentlyReconstructedDiscrepancyEventOne",
    ),
}


def axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert output.count(no_axioms) + (match is not None) == 1, declaration
    if match is None:
        return set()
    return {part.strip() for part in match.group(1).split(",") if part.strip()}


for log_name, declarations in groups.items():
    output = (target / log_name).read_text(encoding="utf-8")
    assert "error:" not in output, log_name
    assert output.count("Declarations are sorry-free!") == len(declarations), log_name
    for declaration in declarations:
        observed = axioms(output, declaration)
        assert observed <= allowed, (declaration, observed)

for log_name in ("Statement.out", "ObligationTree.out", "Proof.out", "AnchorAudit.out"):
    output = (target / log_name).read_text(encoding="utf-8")
    assert "error:" not in output, log_name
    assert "sorryAx" not in output and "declaration uses 'sorry'" not in output, log_name

print(
    "PASS THM-M-1065 network-isolated trust-zero replay: exact statement, conditional "
    "composition, two partial proof bodies, two anchor decisions, and two differential "
    "statement probes are sorry-free with no unexpected axioms"
)
PY
