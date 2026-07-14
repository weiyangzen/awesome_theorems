#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-1021"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m1021-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

mkdir -p "$tmp/External/Bochner" "$tmp/Stage1_Instances/THM-M-1021"
cp "$target/External/Bochner/PositiveDefinite.lean" \
  "$tmp/External/Bochner/PositiveDefinite.lean"
cp "$target/External/Bochner/FejerPD.lean" \
  "$tmp/External/Bochner/FejerPD.lean"
cp "$target/External/Bochner/Main.lean" \
  "$tmp/External/Bochner/Main.lean"
cp "$target/BochnerStatement.lean" \
  "$tmp/Stage1_Instances/THM-M-1021/BochnerStatement.lean"
cp "$target/Proof.lean" "$tmp/Stage1_Instances/THM-M-1021/Proof.lean"
cp "$target/Validation.lean" "$tmp/Stage1_Instances/THM-M-1021/Validation.lean"

lean_bin="$(cd "$lean_root" && lake env which lean)"
lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
[[ -x "$lean_bin" ]] || {
  printf 'missing pinned Lean executable: %s\n' "$lean_bin" >&2
  exit 1
}
[[ -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" ]] || {
  printf 'missing pinned Lean artifact: %s\n' \
    "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean" >&2
  exit 1
}

base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8
  --setenv LC_ALL C.UTF-8 --setenv TZ UTC --setenv LEAN_NUM_THREADS 1
  --chdir "$tmp"
)

compile() {
  local module="$1"
  local module_path="$tmp/$module.lean"
  local output_path="$tmp/${module//\//-}.out"
  mkdir -p "$(dirname "$tmp/$module.olean")"
  "${base[@]}" --setenv LEAN_PATH "$tmp:$lean_path" --setenv PATH "$PATH" \
    "$lean_bin" --trust=0 -t0 -R "$tmp" -o "$tmp/$module.olean" \
    "$module_path" >"$output_path" 2>&1
}

compile External/Bochner/PositiveDefinite
compile External/Bochner/FejerPD
compile External/Bochner/Main
compile Stage1_Instances/THM-M-1021/BochnerStatement
compile Stage1_Instances/THM-M-1021/Proof
compile Stage1_Instances/THM-M-1021/Validation

validation_output="$tmp/Stage1_Instances-THM-M-1021-Validation.out"
cat "$validation_output"

python3 - "$validation_output" <<'PY' >&2
import re
import sys
from pathlib import Path

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")

output = Path(sys.argv[1]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "bochner_theorem",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_forward",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_reverse",
    "AwesomeTheorems.Stage1.THM_M_1021.bochner_exact",
)

assert output.count("Declarations are sorry-free!") == len(declarations)
assert "declaration uses 'sorry'" not in output
assert "sorryAx" not in output and "error:" not in output
reports = re.findall(r"'([^']+)' depends on axioms: \[(.*?)]", output, re.DOTALL)
assert [name for name, _ in reports] == list(declarations), reports
for declaration, values in reports:
    actual = {name.strip() for name in values.split(",") if name.strip()}
    assert actual == allowed, f"unexpected axioms for {declaration}: {actual}"
PY

for module in \
  External/Bochner/PositiveDefinite \
  External/Bochner/FejerPD \
  External/Bochner/Main \
  Stage1_Instances/THM-M-1021/BochnerStatement \
  Stage1_Instances/THM-M-1021/Proof \
  Stage1_Instances/THM-M-1021/Validation
do
  test -s "$tmp/$module.olean"
done
