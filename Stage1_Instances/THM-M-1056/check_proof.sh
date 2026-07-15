#!/usr/bin/env bash
set -euo pipefail

export LC_ALL=C.UTF-8
export TZ=Asia/Shanghai

root=$(git rev-parse --show-toplevel)
here="$root/Stage1_Instances/THM-M-1056"
lean_dir="$root/Formalizations/Lean"
vendor="$here/External/Oseledets"
mathlib="$lean_dir/.lake/packages/mathlib"
tmp=${M1056_REPLAY_TMP:-}
if [ -n "$tmp" ]; then
  test ! -e "$tmp"
  mkdir -p "$tmp"
  cleanup_tmp=false
else
  tmp=$(mktemp -d /tmp/m1056-proof.XXXXXX)
  cleanup_tmp=true
fi
cleanup() {
  if "$cleanup_tmp"; then
    rm -rf "$tmp"
  fi
}
trap cleanup EXIT

source_root="$tmp/source"
vendor_source="$source_root/vendor"
wrapper_source="$source_root/wrapper"
external_out="$tmp/build/external"
wrapper_out="$tmp/build/wrapper"
replay_log="$tmp/replay.log"
mkdir -p "$vendor_source" "$wrapper_source" "$external_out" "$wrapper_out"

base_lean_path=$(cd "$lean_dir" && env -u LEAN_PATH lake env printenv LEAN_PATH)
lean_version=$(cd "$lean_dir" && env -u LEAN_PATH lake env lean --version)
test "$lean_version" = \
  "Lean (version 4.29.0, x86_64-unknown-linux-gnu, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740, Release)"
test "$(git -C "$mathlib" rev-parse HEAD)" = \
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"
test "$(git -C "$mathlib" rev-parse 'HEAD^{tree}')" = \
  "bdc39a3123201dae413a9d9be56ec242c19e5c2b"
test -z "$(git -C "$mathlib" status --short --untracked-files=no)"

# Copy every checked source before compiling so no target-local olean can be
# read or created during the replay.
cp -R "$vendor/." "$vendor_source/"
modules=(
  Statement
  CoordinateBridge
  IntegrabilityBridge
  CocycleBridge
  GrowthBridge
  ExternalInvoke
  ConditionalWrapper
  M1056ProjectionBridge
  ConcreteProjectionPackage
  Proof
)
for module in "${modules[@]}"; do
  cp "$here/$module.lean" "$wrapper_source/$module.lean"
done

test "$(find "$tmp" -name '*.olean' | wc -l)" -eq 0

run_lean() {
  local label=$1
  local lean_path=$2
  local module_root=$3
  local output=$4
  local source=$5
  printf '[compile] %s\n' "$label" | tee -a "$replay_log"
  set +e
  (
    cd "$lean_dir"
    env LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 \
      timeout --foreground --kill-after=10s 900s \
      lake env lean --trust=0 -t0 -R "$module_root" -o "$output" "$source"
  ) 2>&1 | tee -a "$replay_log"
  local status=${PIPESTATUS[0]}
  set -e
  if [ "$status" -ne 0 ]; then
    printf 'FAIL %s (exit %s)\n' "$label" "$status" >&2
    exit "$status"
  fi
  test -s "$output"
}

i=0
while IFS= read -r module; do
  test -n "$module"
  i=$((i + 1))
  relative=${module//.//}
  source="$vendor_source/$relative.lean"
  output="$external_out/$relative.olean"
  mkdir -p "$(dirname "$output")"
  run_lean "external $i/62 $module" \
    "$external_out:$base_lean_path" "$vendor_source" "$output" "$source"
done < "$vendor_source/order.txt"
test "$i" -eq 62
test "$(find "$external_out" -name '*.olean' | wc -l)" -eq 62

for module in "${modules[@]}"; do
  run_lean "target $module" \
    "$wrapper_out:$external_out:$base_lean_path" "$wrapper_source" \
    "$wrapper_out/$module.olean" "$wrapper_source/$module.lean"
done
test "$(find "$wrapper_out" -name '*.olean' | wc -l)" -eq 10

cat > "$tmp/ExactProbe.lean" <<'LEAN'
import Proof

#check (Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic :
  Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget)
#check (Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget :
  Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget)

#print sorries ErgodicTheory.oseledets_splitting
#print sorries Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target
#print sorries Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic
#print sorries Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget
#print axioms ErgodicTheory.oseledets_splitting
#print axioms Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target
#print axioms Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic
#print axioms Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget
LEAN

probe_log="$tmp/exact-probe.out"
set +e
(
  cd "$lean_dir"
  env LEAN_PATH="$wrapper_out:$external_out:$base_lean_path" LEAN_NUM_THREADS=1 \
    timeout --foreground --kill-after=10s 900s \
    lake env lean --trust=0 -t0 -R "$tmp" -o "$tmp/ExactProbe.olean" \
    "$tmp/ExactProbe.lean"
) 2>&1 | tee "$probe_log" | tee -a "$replay_log"
probe_status=${PIPESTATUS[0]}
set -e
test "$probe_status" -eq 0
test -s "$tmp/ExactProbe.olean"

python3 - "$probe_log" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
declarations = (
    "ErgodicTheory.oseledets_splitting",
    "Stage1Instances.THM_M_1056.oseledets_multiplicative_ergodic_target",
    "Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodic",
    "Stage1Instances.THM_M_1056.oseledetsMultiplicativeErgodicTarget",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
assert output.count("Declarations are sorry-free!") == len(declarations), output
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, (declaration, actual)
for prohibited in ("sorryAx", "declaration uses 'sorry'", "error:"):
    if prohibited == "error:":
        assert prohibited not in output.lower()
    else:
        assert prohibited not in output
PY

test -z "$(find "$here" -name '*.olean' -print -quit)"
printf 'TERMINAL_OLEAN_SHA256=%s\n' \
  "$(sha256sum "$external_out/ErgodicTheory/TwoSided/SplittingAssembly.olean" | cut -d' ' -f1)"
printf 'PROOF_OLEAN_SHA256=%s\n' \
  "$(sha256sum "$wrapper_out/Proof.olean" | cut -d' ' -f1)"
printf 'EXTERNAL_OLEAN_AGGREGATE_SHA256=%s\n' \
  "$(cd "$external_out" && find . -name '*.olean' -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -d' ' -f1)"
printf 'WRAPPER_OLEAN_AGGREGATE_SHA256=%s\n' \
  "$(cd "$wrapper_out" && find . -name '*.olean' -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -d' ' -f1)"
printf '%s\n' \
  'PASS THM-M-1056 isolated proof elaboration (62 vendored modules, 10 target modules, --trust=0 -t0)'
