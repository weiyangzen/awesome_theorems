#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0347"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0347-proof.XXXXXX)"
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

cp "$target"/{Statement,AtlasFourierSeries,AtlasAxiomProbe,Proof}.lean "$tmp/"
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
run_lean ".:$lean_path" Proof.lean > proof.out

python3 - "$tmp/atlas-axioms.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")

allowed = {"propext", "Classical.choice", "Quot.sound"}
groups = {
    Path(sys.argv[1]): (
        "fejer_kernel_properties",
        "cesaroMean_eq_fejer_convolution",
        "fejerKernel_eq_ofReal",
        "integral_norm_fejerKernel",
        "cesaroMean_uniform_bound",
        "fejer_uniform_convergence",
    ),
    Path(sys.argv[2]): (
        "symmetricFourierPartialSum_apply",
        "fejerMean_apply",
        "fejerTheorem",
    ),
}

for path, short_names in groups.items():
    output = path.read_text(encoding="utf-8")
    assert "sorryAx" not in output, f"{path.name}: sorryAx in axiom closure"
    assert "error:" not in output, f"{path.name}: Lean error"
    for short_name in short_names:
        match = re.search(
            rf"'[^']*\.?{re.escape(short_name)}' depends on axioms: \[(.*?)]",
            output,
            re.DOTALL,
        )
        assert match, f"{path.name}: missing axiom report for {short_name}"
        actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
        assert actual == allowed, f"{path.name}: unexpected axioms for {short_name}: {actual}"

print("PASS THM-M-0347 Lean proof: exact root and eight support declarations elaborate")
PY

python3 "$target/check_proof.py"
