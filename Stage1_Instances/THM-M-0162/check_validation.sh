#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0162"
lean_root="$repo_root/Formalizations/Lean"
mathlib="$lean_root/.lake/packages/mathlib"
tmp="$(mktemp -d /tmp/stage1-m0162-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

mkdir -p "$tmp/Stage1_Instances/THM-M-0162" "$tmp/home"
cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean \
  "$tmp/Stage1_Instances/THM-M-0162/"

# Resolve Lean through the pinned mathlib Lake environment while denying
# network access even during discovery. This avoids the root manifest's
# unrelated, currently unavailable flt-regular checkout.
lake_bin="${STAGE1_M0162_LAKE_BIN:-$(command -v lake)}"
lean_bin_expected="${STAGE1_M0162_LEAN_BIN:-}"
[[ -x "$lake_bin" ]] || {
  printf 'missing pinned Lake launcher: %s\n' "$lake_bin" >&2
  exit 1
}
lean_bin="$(
  bwrap --ro-bind / / --dev /dev --proc /proc --unshare-net --die-with-parent \
    --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
    --chdir "$mathlib" "$lake_bin" env which lean
)"
if [[ -n "$lean_bin_expected" && "$lean_bin" != "$lean_bin_expected" ]]; then
  printf 'Lake resolved an unexpected Lean executable: %s\n' "$lean_bin" >&2
  exit 1
fi
[[ -x "$lean_bin" ]] || {
  printf 'missing pinned Lean executable: %s\n' "$lean_bin" >&2
  exit 1
}
[[ -f "$mathlib/.lake/build/lib/lean/Mathlib.olean" ]] || {
  printf 'missing pinned Lean artifact: %s\n' \
    "$mathlib/.lake/build/lib/lean/Mathlib.olean" >&2
  exit 1
}

# The canonical root package set contains mathlib's built dependencies. Build
# an explicit read-only path so Lake never attempts package discovery or fetch
# inside the network-denied replay.
paths=("$mathlib/.lake/build/lib/lean")
for path in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  [[ -d "$path" ]] && paths+=("$path")
done
paths+=("$(dirname "$(dirname "$lean_bin")")/lib/lean")
lean_path="$(IFS=:; printf '%s' "${paths[*]}")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv HOME "$tmp/home"
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)

compile() {
  local module="$1"
  local path="$lean_path"
  if [[ "$module" != "Statement" ]]; then
    path="$tmp:$lean_path"
  fi
  "${base[@]}" --setenv LEAN_PATH "$path" \
    "$lean_bin" --trust=0 -t0 -R "$tmp" \
    -o "$tmp/Stage1_Instances/THM-M-0162/$module.olean" \
    "$tmp/Stage1_Instances/THM-M-0162/$module.lean"
}

compile Statement > "$tmp/statement.out"
compile ObligationTree > "$tmp/obligation-tree.out"
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
    "Stage1Instances.THM_M_0162.tangentEquation",
    "Stage1Instances.THM_M_0162.normalEquation",
    "Stage1Instances.THM_M_0162.binormalEquation",
    "Stage1Instances.THM_M_0162.frenetSerret",
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
    assert observed_axioms(combined, declaration) == allowed, declaration
assert validation.count("Declarations are sorry-free!") == len(declarations)
assert "declaration uses 'sorry'" not in combined
assert "sorryAx" not in combined
assert "error:" not in combined
PY

for module in Statement ObligationTree Proof Validation; do
  test -s "$tmp/Stage1_Instances/THM-M-0162/$module.olean"
done

printf 'Statement.olean sha256: '
sha256sum "$tmp/Stage1_Instances/THM-M-0162/Statement.olean" | cut -d' ' -f1
printf 'ObligationTree.olean sha256: '
sha256sum "$tmp/Stage1_Instances/THM-M-0162/ObligationTree.olean" | cut -d' ' -f1
printf 'Proof.olean sha256: '
sha256sum "$tmp/Stage1_Instances/THM-M-0162/Proof.olean" | cut -d' ' -f1
printf 'Validation.olean sha256: '
sha256sum "$tmp/Stage1_Instances/THM-M-0162/Validation.olean" | cut -d' ' -f1
printf 'PASS network-denied trust-zero fresh-output replay\n'
