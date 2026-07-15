#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0957"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(/usr/bin/mktemp -d /tmp/stage1-m0957-validation.XXXXXX)"
cleanup() {
  /usr/bin/rm -rf "$tmp"
}
trap cleanup EXIT
umask 022

/usr/bin/cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"
/usr/bin/mkdir "$tmp/home"

cd "$lean_root"
elan_bin="/home/sansha-2/.elan/bin/elan"
[[ -x "$elan_bin" ]] || {
  printf 'missing pinned Elan executable: %s\n' "$elan_bin" >&2
  exit 1
}
[[ "$(/usr/bin/sha256sum "$elan_bin")" == \
  "840179e70803ef373c2ec53342d6a45ea7d022533e4145489fc1278b4f716385  $elan_bin" ]] || {
  printf 'pinned Elan digest mismatch\n' >&2
  exit 1
}
lake_bin="$(
  /usr/bin/env -i HOME=/home/sansha-2 PATH=/usr/bin:/bin \
    ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
    "$elan_bin" which lake
)"
toolchain_bin="${lake_bin%/*}"
lean_bin="$toolchain_bin/lean"
[[ "$(/usr/bin/sha256sum "$lake_bin")" == \
  "a608ff084d7e2af228b92a29d7c2fd083ba0580e46889175ec74a81678c98359  $lake_bin" ]] || {
  printf 'pinned Lake digest mismatch\n' >&2
  exit 1
}
[[ "$(/usr/bin/sha256sum "$lean_bin")" == \
  "3e0d0d3d801675359f2d4cf9815bfdb417b20b92fdd9d48b3b14c95bbae28bbf  $lean_bin" ]] || {
  printf 'pinned Lean digest mismatch\n' >&2
  exit 1
}
[[ "$(/usr/bin/sha256sum /usr/bin/bwrap)" == \
  "0abea81db798ebf6b4742ac0664802d97521547a353c2a0dbdc21d76cbbfd2c0  /usr/bin/bwrap" ]] || {
  printf 'Bubblewrap digest mismatch\n' >&2
  exit 1
}
lean_path="$(
  /usr/bin/env -i HOME=/home/sansha-2 PATH="$toolchain_bin:/usr/bin:/bin" \
    ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC \
    "$lake_bin" env printenv LEAN_PATH
)"
[[ -x "$lean_bin" ]] || {
  printf 'missing pinned Lean executable: %s\n' "$lean_bin" >&2
  exit 1
}
[[ -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" ]] || {
  printf 'missing pinned Lean artifact: %s\n' \
    "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" >&2
  exit 1
}
tmp="$(/usr/bin/realpath "$tmp")"

base=(
  /usr/bin/bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --clearenv --setenv HOME "$tmp/home"
  --setenv PATH "$toolchain_bin:/usr/bin:/bin"
  --setenv ELAN_TOOLCHAIN leanprover/lean4:v4.29.0
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --setenv LEAN_NUM_THREADS 1 --chdir "$lean_root"
)

compile() {
  local module="$1"
  local output="$2"
  local path="$lean_path"
  if [[ "$module" != "Statement" && "$module" != "ObligationTree" ]]; then
    path="$tmp:$lean_path"
  fi
  if ! "${base[@]}" \
    "$lake_bin" env /usr/bin/env LEAN_PATH="$path" \
    "$lean_bin" --trust=0 -t0 -R "$tmp" \
      -o "$tmp/$module.olean" "$tmp/$module.lean" >"$output" 2>&1; then
    /usr/bin/cat "$output" >&2
    return 1
  fi
}

compile Statement "$tmp/statement.out"
compile ObligationTree "$tmp/obligation-tree.out"
compile Proof "$tmp/proof.out"
compile Validation "$tmp/validation.out"
/usr/bin/cat "$tmp/validation.out"

/usr/bin/python3 -I -B - "$tmp/proof.out" "$tmp/validation.out" <<'PY' >&2
import hashlib
import json
import re
import sys
from pathlib import Path

proof = Path(sys.argv[1]).read_text(encoding="utf-8")
validation = Path(sys.argv[2]).read_text(encoding="utf-8")
combined = proof + validation
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "Stage1Instances.THM_M_0957.sourceThreeAPFree_iff_threeAPFree",
    "Stage1Instances.THM_M_0957.behrendConstructionTarget_iff_finiteSet",
    "Behrend.bound_aux",
    "Stage1Instances.THM_M_0957_ObligationTree.dimensionControl_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.rpowNormalization_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyRpowIdentity_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxySlackAbsorption_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.ambientFit_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearCeiling_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearIncrementAbsorption_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.dimensionSlack_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.logDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.reciprocalBalancedCore_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.reciprocalDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.radixBase_eventually_one",
    "Stage1Instances.THM_M_0957_ObligationTree.radixNonzero_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.radixFloor_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.quantitativeConstruction_installed",
    "Stage1Instances.THM_M_0957_ObligationTree.indexMonotonicity_installed",
    "Stage1Instances.THM_M_0957_ObligationTree.parameterAdmissibility_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyLogLower_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.linearDimensionLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.subleadingLoss_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.optimalExponentBridge_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.proxyAsymptotic_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.ratioAsymptotic_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.sharpEstimate_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.sharpParameter_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.exactAssembly_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.exactRoot_proof",
    "Stage1Instances.THM_M_0957_ObligationTree.behrendConstructionTarget_proof",
)


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


for declaration in declarations:
    actual = observed_axioms(combined, declaration)
    assert actual <= allowed, (declaration, actual)
assert observed_axioms(
    combined,
    "Stage1Instances.THM_M_0957_ObligationTree.behrendConstructionTarget_proof",
) == allowed
assert validation.count("Declarations are sorry-free!") == len(declarations)
assert "declaration uses 'sorry'" not in combined
assert "sorryAx" not in combined
assert "error:" not in combined.lower()
assert re.search(
    r"VALIDATION_CLOSURE roots=4 declarations=\d+ modules=\d+", validation
)
assert "VALIDATION_CLOSURE axioms=[propext, Classical.choice, Quot.sound]" in validation
assert "VALIDATION_CLOSURE bodyless_nonaxioms=[]" in validation
assert "VALIDATION_CLOSURE unsafe=[]" in validation

tmp = Path(sys.argv[1]).parent
artifacts = {}
for module, output_name in (
    ("Statement", "statement.out"),
    ("ObligationTree", "obligation-tree.out"),
    ("Proof", "proof.out"),
    ("Validation", "validation.out"),
):
    output = (tmp / output_name).read_bytes()
    artifacts[module] = {
        "stdout_bytes": len(output),
        "stdout_sha256": hashlib.sha256(output).hexdigest(),
        "olean_bytes": (tmp / f"{module}.olean").stat().st_size,
        "olean_sha256": hashlib.sha256(
            (tmp / f"{module}.olean").read_bytes()
        ).hexdigest(),
    }
print(
    "VALIDATION_ARTIFACTS="
    + json.dumps(artifacts, sort_keys=True, separators=(",", ":"))
)
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/ObligationTree.olean"
test -s "$tmp/Proof.olean"
test -s "$tmp/Validation.olean"
