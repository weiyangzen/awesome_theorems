#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1291"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1291-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,Proof,Validation}.lean "$tmp/"

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
tmp="$(realpath "$tmp")"

# Lake's Lean wrapper requires input paths below the package root. Bind the
# disposable directory at a fresh package-root path while keeping /tmp storage.
mount_tmp="$lean_root/.m1291-validation.$(basename "$tmp")"
mkdir "$mount_tmp"
trap 'rmdir "$mount_tmp" 2>/dev/null || true; rm -rf "$tmp"' EXIT

base=(
  bwrap --ro-bind / / --bind "$tmp" "$mount_tmp" --dev /dev --proc /proc
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
    lake env lean --trust=0 -o "$mount_tmp/$module.olean" "$mount_tmp/$module.lean"
}

compile Statement > "$tmp/statement.out"
compile Proof > "$tmp/proof.out"
compile Validation > "$tmp/validation.out"
cat "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/proof.out" "$tmp/validation.out" <<'PY' >&2
import re
import sys
from pathlib import Path

proof = Path(sys.argv[1]).read_text(encoding="utf-8")
validation = Path(sys.argv[2]).read_text(encoding="utf-8")
combined = proof + validation
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "Stage1Instances.THM_M_1291.rpow_add_le_weighted",
    "Stage1Instances.THM_M_1291.abs_rpow_norm_sub_rpow_norm_sub_le_weighted",
    "Stage1Instances.THM_M_1291.rpow_coeff_tendsto_zero",
    "Stage1Instances.THM_M_1291.truncatedError_nonneg",
    "Stage1Instances.THM_M_1291.truncatedError_le",
    "Stage1Instances.THM_M_1291.integrable_of_ae_tendsto_of_uniform_integral_bound",
    "Stage1Instances.THM_M_1291.abs_rpow_norm_add_sub_rpow_norm_le",
    "Stage1Instances.THM_M_1291.splittingLimit_subunit",
    "Stage1Instances.THM_M_1291.splittingLimit_superunit",
    "Stage1Instances.THM_M_1291.brezisLiebTarget_proof",
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
    combined, "Stage1Instances.THM_M_1291.brezisLiebTarget_proof"
) == allowed
assert validation.count("Declarations are sorry-free!") == len(declarations)
assert "declaration uses 'sorry'" not in combined
assert "sorryAx" not in combined
assert "error:" not in combined
PY

test -s "$tmp/Statement.olean"
test -s "$tmp/Proof.olean"
test -s "$tmp/Validation.olean"
