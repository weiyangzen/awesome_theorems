#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1244"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1244-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,ObligationTree,Proof,ProofAudit,Validation}.lean "$tmp/"
cp -R "$target/SLT" "$tmp/SLT"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --clearenv
  --setenv HOME "$tmp" --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)

run_lean() {
  local module_path="$1"
  local log="$2"
  shift 2
  timeout 840 "${base[@]}" --setenv LEAN_PATH "$module_path" \
    "$lean_bin" --trust=0 -t0 -R "$tmp" "$@" > "$tmp/$log" 2>&1
}

modules=(
  SLT/EfronStein
  SLT/ConvergenceL1Subseq
  SLT/GaussianLSI/Entropy
  SLT/GaussianLSI/TwoPoint
  SLT/GaussianPoincare/LevyContinuity
  SLT/GaussianPoincare/RademacherApprox
  SLT/GaussianPoincare/EfronSteinApp
  SLT/GaussianPoincare/TaylorBound
  SLT/GaussianPoincare/Limit
  SLT/GaussianLSI/BernoulliLSI
  SLT/GaussianLSI/OneDimGLSICompSmo
  SLT/MeasureInfrastructure
  SLT/GaussianMeasure
  SLT/GaussianSobolevDense/Defs
  SLT/GaussianSobolevDense/Cutoff
  SLT/GaussianSobolevDense/Mollification
  SLT/GaussianSobolevDense/Density
  SLT/GaussianLSI/OneDimGLSI
  SLT/GaussianLSI/DualityEntropy
  SLT/GaussianLSI/DualEntApp
  SLT/GaussianLSI/SubAddEnt/Basic
  SLT/GaussianLSI/SubAddEnt/Decomposition
  SLT/GaussianLSI/SubAddEnt/Subadditivity
  SLT/GaussianLSI/TensorizedGLSI
)
run_lean "$lean_path" statement.out -o Statement.olean Statement.lean
run_lean "$tmp:$lean_path" obligation.out -o ObligationTree.olean ObligationTree.lean
for module in "${modules[@]}"; do
  run_lean "$tmp:$lean_path" "${module//\//-}.out" \
    -o "$module.olean" "$module.lean"
done
run_lean "$tmp:$lean_path" proof.out -o Proof.olean Proof.lean
run_lean "$tmp:$lean_path" audit.out ProofAudit.lean

# The differential replay must not resolve the local Proof module.
rm -f "$tmp/Proof.olean" "$tmp/Proof.ilean" "$tmp/Proof.lean"
test ! -e "$tmp/Proof.olean" && test ! -e "$tmp/Proof.lean"
run_lean "$tmp:$lean_path" validation.out Validation.lean

cat "$tmp"/{audit,validation}.out

python3 - "$tmp/audit.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

audit = Path(sys.argv[1]).read_text(encoding="utf-8")
validation = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
audit_declarations = (
    "Stage1Instances.THM_M_1244.gaussianLogSobolevTarget_iff_expandedTarget",
    "Stage1Instances.THM_M_1244.gaussianLogSobolevTarget_of_packages",
    "GaussianLSI.gaussian_logSobolev_W12_pi",
    "Stage1Instances.THM_M_1244.coordinateLogSobolevPackage",
    "Stage1Instances.THM_M_1244.coordinateToOperatorEnergyPackage",
    "Stage1Instances.THM_M_1244.gaussianLogSobolev",
)
differential_declarations = (
    "Stage1Instances.THM_M_1244.Validation.independentlyReconstructedGaussianLogSobolev",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    no_axioms = f"'{declaration}' does not depend on any axioms"
    pattern = re.compile(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        re.DOTALL,
    )
    matches = pattern.findall(output)
    assert output.count(no_axioms) + len(matches) == 1, declaration
    if not matches:
        return set()
    return {name.strip() for name in matches[0].split(",") if name.strip()}


for declaration in audit_declarations:
    assert observed_axioms(audit, declaration) <= allowed, declaration
for declaration in differential_declarations:
    assert observed_axioms(validation, declaration) == allowed, declaration
assert audit.count("Declarations are sorry-free!") == len(audit_declarations)
assert validation.count("Declarations are sorry-free!") == len(differential_declarations)
combined = audit + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
print("PASS axiom profile: seven checked declarations stay within propext, Classical.choice, and Quot.sound")
print("PASS kernel sorry traversal: target, composition, vendored terminal, packages, and both exact roots are sorry-free")
PY
