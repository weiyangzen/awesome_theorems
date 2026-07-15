#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0819"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0819-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT
umask 022

cp "$target"/{Statement,FiniteDilworth,Proof,Validation}.lean "$tmp/"

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
base=(
  bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc
  --unshare-net --die-with-parent --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8
  --setenv TZ UTC --setenv LEAN_NUM_THREADS 1 --chdir "$tmp"
)

compile() {
  local module="$1"
  local path="$lean_path"
  if [[ "$module" != "Statement" && "$module" != "FiniteDilworth" ]]; then
    path="$tmp:$lean_path"
  fi
  timeout --signal=TERM --kill-after=5s 240s \
    "${base[@]}" --setenv LEAN_PATH "$path" \
      "$lean_bin" --trust=0 -R "$tmp" -o "$tmp/$module.olean" "$tmp/$module.lean"
}

compile Statement > "$tmp/statement.out"
compile FiniteDilworth > "$tmp/finite.out"
compile Proof > "$tmp/proof.out"
compile Validation > "$tmp/validation.out"
cat "$tmp/validation.out"

python3 - "$tmp/validation.out" <<'PY' >&2
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "minAntichainPartition_eq_chainHeight",
    "minChainPartition_eq_antichainWidth",
    "Stage1Instances.THM_M_0819_Proof.dilworthPrimary",
)

for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, (declaration, actual)

assert output.count("Declarations are sorry-free!") == len(declarations)
assert "declaration uses 'sorry'" not in output
assert "sorryAx" not in output
assert "error:" not in output
PY

for module in Statement FiniteDilworth Proof Validation; do
  test -s "$tmp/$module.olean"
done
printf 'PASS THM-M-0819 network-isolated trust-zero validation replay\n'
