#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1285"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1285-validation.XXXXXX)"

cleanup() {
  rm -rf "$tmp"
}
trap cleanup EXIT
umask 022

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
[[ -x "$lean_bin" ]] || {
  printf 'missing pinned Lean executable: %s\n' "$lean_bin" >&2
  exit 1
}
[[ -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" ]] || {
  printf 'missing pinned Lean artifact: %s\n' \
    "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" >&2
  exit 1
}

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$lean_root"
)

compile() {
  local module="$1"
  local path="$lean_path"
  if [[ "$module" != "Statement" ]]; then
    path="$tmp:$lean_path"
  fi
  "${base[@]}" --setenv LEAN_PATH "$path" --setenv PATH "$PATH" \
    timeout --foreground 420 "$lean_bin" --trust=0 -t0 -R "$tmp" \
    -o "$tmp/$module.olean" "$tmp/$module.lean"
}

compile Statement > "$tmp/statement.out"
compile ObligationTree > "$tmp/obligation-tree.out"
compile Proof > "$tmp/proof.out"
compile Validation > "$tmp/validation.out"
cat "$tmp/proof.out" "$tmp/obligation-tree.out" "$tmp/validation.out"

python3 - "$tmp/validation.out" <<'PY' >&2
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_iff_expandedTarget",
    "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_of_construction",
    "Stage1Instances.THM_M_1285.isRadial_profile",
    "Stage1Instances.THM_M_1285.isRadiallyNonincreasing_profile",
    "Stage1Instances.THM_M_1285.measurable_profile",
    "Stage1Instances.THM_M_1285.distribution_antitone",
    "Stage1Instances.THM_M_1285.iUnion_strictSuperlevel_gt",
    "Stage1Instances.THM_M_1285.distribution_iSup_rat_gt",
    "Stage1Instances.THM_M_1285.volume_ball_radiusForVolume",
    "Stage1Instances.THM_M_1285.radiusForVolume_nonneg",
    "Stage1Instances.THM_M_1285.radiusForVolume_mono",
    "Stage1Instances.THM_M_1285.starProfile_measurable",
    "Stage1Instances.THM_M_1285.starProfile_antitone",
    "Stage1Instances.THM_M_1285.strictSuperlevel_starProfile",
    "Stage1Instances.THM_M_1285.measure_strictSuperlevel_starProfile",
    "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_proof",
)


def observed_axioms(declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    if match is None:
        assert no_axioms in output, f"missing axiom report for {declaration}"
        return set()
    return {item.strip() for item in match.group(1).split(",") if item.strip()}


for declaration in declarations:
    actual = observed_axioms(declaration)
    assert actual <= allowed, (declaration, actual)
assert observed_axioms(
    "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_proof"
) == allowed
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "declaration uses 'sorry'" not in output
assert "sorryAx" not in output
assert "error:" not in output
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
test -s "$tmp/Validation.olean"
