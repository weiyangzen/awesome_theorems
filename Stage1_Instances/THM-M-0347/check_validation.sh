#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0347"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0347-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

toolchain_root="${HOME}/.elan/toolchains/leanprover--lean4---v4.29.0"
lean_bin="$toolchain_root/bin/lean"
lean_dirs=(
  "$lean_root/.lake/packages/batteries/.lake/build/lib/lean"
  "$lean_root/.lake/packages/Qq/.lake/build/lib/lean"
  "$lean_root/.lake/packages/aesop/.lake/build/lib/lean"
  "$lean_root/.lake/packages/proofwidgets/.lake/build/lib/lean"
  "$lean_root/.lake/packages/importGraph/.lake/build/lib/lean"
  "$lean_root/.lake/packages/LeanSearchClient/.lake/build/lib/lean"
  "$lean_root/.lake/packages/plausible/.lake/build/lib/lean"
  "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean"
  "$lean_root/.lake/build/lib/lean"
  "$toolchain_root/lib/lean"
)

test -x "$lean_bin"
for dir in "${lean_dirs[@]}"; do test -d "$dir"; done
lean_path="$(IFS=:; echo "${lean_dirs[*]}")"

cp "$target"/{Statement,AtlasFourierSeries,AtlasAxiomProbe,ObligationTree,Proof,Validation}.lean "$tmp/"
cd "$tmp"

run_lean() {
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc \
    --unshare-net --die-with-parent --clearenv --setenv HOME "$tmp" \
    --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
    --setenv LEAN_NUM_THREADS 1 --setenv LEAN_PATH "$1" --chdir "$tmp" \
    timeout 420s "$lean_bin" --trust=0 "${@:2}"
}

run_lean "$lean_path" -o Statement.olean Statement.lean >/dev/null
run_lean "$lean_path" -o AtlasFourierSeries.olean AtlasFourierSeries.lean \
  > atlas-source.out
run_lean ".:$lean_path" AtlasAxiomProbe.lean > atlas-axioms.out
run_lean ".:$lean_path" -o ObligationTree.olean ObligationTree.lean \
  > obligation.out
run_lean ".:$lean_path" Proof.lean > proof.out
run_lean ".:$lean_path" Validation.lean > validation.out

cat obligation.out atlas-axioms.out proof.out validation.out

python3 - "$tmp/obligation.out" "$tmp/atlas-axioms.out" \
  "$tmp/proof.out" "$tmp/validation.out" <<'PY'
from pathlib import Path
import re
import sys

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")

obligation, atlas, proof, validation = [
    Path(name).read_text(encoding="utf-8") for name in sys.argv[1:]
]
allowed = {"propext", "Classical.choice", "Quot.sound"}
groups = (
    (obligation, (
        "Stage1Instances.THM_M_0347.ObligationTree.root_of_uniformFejerEstimate",
    )),
    (atlas, (
        "FourierSeries.fejer_kernel_properties",
        "FourierSeries.cesaroMean_eq_fejer_convolution",
        "fejerKernel_eq_ofReal",
        "integral_norm_fejerKernel",
        "cesaroMean_uniform_bound",
        "fejer_uniform_convergence",
    )),
    (proof, (
        "Stage1Instances.THM_M_0347.symmetricFourierPartialSum_apply",
        "Stage1Instances.THM_M_0347.fejerMean_apply",
        "Stage1Instances.THM_M_0347.fejerTheorem",
    )),
    (validation, (
        "FourierSeries.fejer_kernel_properties",
        "FourierSeries.cesaroMean_eq_fejer_convolution",
        "fejerKernel_eq_ofReal",
        "integral_norm_fejerKernel",
        "cesaroMean_uniform_bound",
        "fejer_uniform_convergence",
        "Stage1Instances.THM_M_0347.Validation.reconstructedPartialSum",
        "Stage1Instances.THM_M_0347.Validation.reconstructedMean",
        "Stage1Instances.THM_M_0347.Validation.reconstructedFejerTheorem",
    )),
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for output, declarations in groups:
    for declaration in declarations:
        assert observed_axioms(output, declaration) == allowed, declaration

assert proof.count("depends on axioms") == 3
assert validation.count("Declarations are sorry-free!") == 9
combined = obligation + atlas + proof + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
print("PASS THM-M-0347 network-isolated trust-zero Lean validation")
PY
