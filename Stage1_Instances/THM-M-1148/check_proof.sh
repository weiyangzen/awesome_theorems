#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1148"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1148-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

toolchain_root="${HOME}/.elan/toolchains/leanprover--lean4---v4.29.0"
lean_bin="$toolchain_root/bin/lean"
mathlib_build="$lean_root/.lake/packages/mathlib/.lake/build/lib/lean"
lean_dirs=(
  "$lean_root/.lake/packages/batteries/.lake/build/lib/lean"
  "$lean_root/.lake/packages/Qq/.lake/build/lib/lean"
  "$lean_root/.lake/packages/aesop/.lake/build/lib/lean"
  "$lean_root/.lake/packages/proofwidgets/.lake/build/lib/lean"
  "$lean_root/.lake/packages/importGraph/.lake/build/lib/lean"
  "$lean_root/.lake/packages/LeanSearchClient/.lake/build/lib/lean"
  "$lean_root/.lake/packages/plausible/.lake/build/lib/lean"
  "$mathlib_build"
  "$lean_root/.lake/build/lib/lean"
  "$toolchain_root/lib/lean"
)

test -x "$lean_bin"
test -d "$mathlib_build/Mathlib"
for dir in "${lean_dirs[@]}"; do test -d "$dir"; done
lean_path="$(IFS=:; echo "${lean_dirs[*]}")"

cp "$target"/{Statement,PoissonUnitDisk,Proof}.lean "$tmp/"

cd "$tmp"

run_lean() {
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc \
    --unshare-net --die-with-parent --clearenv --setenv HOME "$tmp" \
    --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
    --setenv LEAN_NUM_THREADS 1 --setenv LEAN_PATH "$1" --chdir "$tmp" \
    timeout 420s "$lean_bin" --trust=0 "${@:2}"
}

run_lean "$lean_path" -o Statement.olean Statement.lean >/dev/null
run_lean "$lean_path" -o PoissonUnitDisk.olean PoissonUnitDisk.lean \
  > poisson-unit-disk.out
run_lean ".:$lean_path" Proof.lean > proof.out

python3 - "$tmp/poisson-unit-disk.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")

allowed = {"propext", "Classical.choice", "Quot.sound"}
groups = {
    Path(sys.argv[1]): (
        "poissonIntegral_eq_re_herglotzIntegral",
        "herglotzIntegral_differentiableOn",
        "poissonIntegral_harmonic",
        "unitDiskExtension_harmonic",
        "unitDiskExtension_eqOn_sphere",
        "unitDiskExtension_continuousOn",
        "unitKernelMass",
        "unitPoissonKernel_nonneg",
        "boundaryData_uniformContinuousOn",
        "continuous_extension_of_sphere",
        "invMobiusAngle_mobiusTransform_core",
        "poissonIntegral_eq_circleAverage_mobiusTransform",
        "mobiusTransform_tendsto_on_circle",
        "circleAverage_mobiusTransform_tendsto",
        "poissonIntegral_tendsto_boundary",
        "bounded_continuous_extension_of_sphere",
        "unitDiskConstruction",
        "harmonicOnNhd_affine_pullback",
        "continuousOn_affine_pullback",
        "eqOn_affine_pullback",
        "generalDiskConstruction",
    ),
    Path(sys.argv[2]): (
        "interiorFormula_of_harmonicContOnCl_of_eqOn",
        "dirichletExtension_to_root",
        "rootTarget_to_frozen",
        "dirichletExtension_to_frozen",
        "dirichletExtension",
        "poissonIntegralFormula",
        "unitDiskConstruction_of_boundaryConvergence",
    ),
}

for path, short_names in groups.items():
    output = path.read_text(encoding="utf-8")
    assert "sorryAx" not in output, f"{path.name}: sorryAx in axiom closure"
    assert "error:" not in output, f"{path.name}: Lean error"
    for short_name in short_names:
        match = re.search(
            rf"'[^']*\.{re.escape(short_name)}' depends on axioms: \[(.*?)]",
            output,
            re.DOTALL,
        )
        assert match, f"{path.name}: missing axiom report for {short_name}"
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual == allowed, f"{path.name}: unexpected axioms for {short_name}: {actual}"

print("PASS THM-M-1148 Lean proof: 28 declarations elaborate; axioms match policy")
PY

python3 "$target/check_proof.py"
