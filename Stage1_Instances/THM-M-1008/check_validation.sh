#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1008"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d "$lean_root/.m1008-validation.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

lean_bin="${HOME}/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean"
lean_paths=("$lean_root/.lake/build/lib/lean")
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  lean_paths+=("$lean_root/.lake/packages/$package/.lake/build/lib/lean")
done
lean_path="$(IFS=:; printf '%s' "${lean_paths[*]}")"
test -x "$lean_bin"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/IdentDistribIndep.olean"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Probability/Independence/ZeroOne.olean"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev-bind /dev /dev --proc /proc
  --unshare-net --die-with-parent --new-session
  --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC
  --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)

"${base[@]}" --setenv LEAN_PATH "$lean_path" \
  "$lean_bin" --trust=0 -o Statement.olean Statement.lean >/dev/null
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o ObligationTree.olean ObligationTree.lean > "$tmp/obligation.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 -o Proof.olean Proof.lean > "$tmp/proof.out"
"${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" \
  "$lean_bin" --trust=0 Validation.lean > "$tmp/validation.out"

python3 - "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

obligation = Path(sys.argv[1]).read_text(encoding="utf-8")
proof = Path(sys.argv[2]).read_text(encoding="utf-8")
validation = Path(sys.argv[3]).read_text(encoding="utf-8")
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


for declaration in (
    "Stage1Instances.THM_M_1008.zeroOne_of_selfIndependence",
    "Stage1Instances.THM_M_1008.root_of_selfIndependencePackage",
):
    assert observed_axioms(obligation, declaration) == allowed, declaration

root = "Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget"
probe = "Stage1Instances.THM_M_1008.Validation.exactRootTypeProbe"
assert observed_axioms(proof, root) == allowed
assert observed_axioms(validation, root) == allowed
assert observed_axioms(validation, probe) == allowed
assert validation.count("Declarations are sorry-free!") == 2
combined = obligation + proof + validation
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined

print("PASS THM-M-1008 network-isolated narrow kernel replay")
print("PASS exact root/type probe: propext, Classical.choice, Quot.sound")
print("PASS transitive sorry check: proof root and type probe are sorry-free")
PY
