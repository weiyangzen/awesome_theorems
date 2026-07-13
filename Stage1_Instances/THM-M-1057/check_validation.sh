#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1057"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1057-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,MaximalErgodic,Birkhoff,KingmanFekete,KingmanDerriennic,KingmanCompanion,KingmanBlockSqueeze,KingmanCore,KingmanMeans,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
toolchain="$(tr -d '[:space:]' < lean-toolchain)"
lean_bin="$(ELAN_TOOLCHAIN="$toolchain" elan which lean)"
toolchain_lib="$(dirname "$(dirname "$lean_bin")")/lib/lean"
lean_path=""
for package in batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do
  path="$lean_root/.lake/packages/$package/.lake/build/lib/lean"
  [[ -d "$path" ]] || { printf 'missing pinned Lean artifact: %s\n' "$path" >&2; exit 1; }
  lean_path="${lean_path:+$lean_path:}$(realpath "$path")"
done
root_lib="$lean_root/.lake/build/lib/lean"
[[ -d "$root_lib" ]] || { printf 'missing pinned Lean artifact: %s\n' "$root_lib" >&2; exit 1; }
lean_path="$lean_path:$(realpath "$root_lib"):$toolchain_lib"
tmp="$(realpath "$tmp")"

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)
compile() {
  local module="$1"
  local path="$lean_path"
  if [[ "$module" != "Statement" ]]; then
    path="$tmp:$lean_path"
  fi
  "${base[@]}" --setenv LEAN_PATH "$path" \
    "$lean_bin" --trust=0 -o "$module.olean" "$module.lean"
}

compile Statement >/dev/null
compile ObligationTree > "$tmp/obligation.out"
for module in MaximalErgodic Birkhoff KingmanFekete KingmanDerriennic \
  KingmanCompanion KingmanBlockSqueeze KingmanCore KingmanMeans; do
  compile "$module" >/dev/null
done
compile Proof > "$tmp/proof.out"
compile Validation > "$tmp/validation.out"
cat "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out"

python3 - "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY' >&2
import re
import sys
from pathlib import Path

obligation = Path(sys.argv[1]).read_text(encoding="utf-8")
proof = Path(sys.argv[2]).read_text(encoding="utf-8")
validation = Path(sys.argv[3]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "Stage1Instances.THM_M_1057.root_of_pointwiseLimitPackage",
    "ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg",
    "ErgodicTheory.tendsto_birkhoffAverage_ae",
    "ErgodicTheory.tendsto_kingman",
    "ErgodicTheory.tendsto_kingman_ergodic",
    "ErgodicTheory.tendsto_kingman_ergodic_means",
    "Stage1Instances.THM_M_1057.pointwiseLimitPackage",
    "Stage1Instances.THM_M_1057.kingmanTarget",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for declaration in declarations:
    assert observed_axioms(obligation + proof + validation, declaration) == allowed, declaration

assert proof.count("Declarations are sorry-free!") == 3
assert validation.count("Declarations are sorry-free!") == len(declarations)
combined = obligation + proof + validation
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
