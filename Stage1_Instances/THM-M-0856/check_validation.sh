#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0856"
lean_root="$repo_root/Formalizations/Lean"

if [[ "${1:-}" != "--lean-only" ]]; then
  exec bwrap --ro-bind / / --bind /tmp /tmp --dev /dev --proc /proc \
    --unshare-net --die-with-parent \
    --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
    --setenv STAGE1_NETWORK_ISOLATED 1 --chdir "$repo_root" \
    python3 -B Stage1_Instances/THM-M-0856/check_validation.py
fi
shift

tmp="$(mktemp -d /tmp/stage1-m0856-validation.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof,Validation}.lean "$tmp/"

cd "$lean_root"
lean_bin="$(lake env which lean)"
lean_path="$(lake env printenv LEAN_PATH)"
tmp="$(realpath "$tmp")"

run_lean() {
  local module_path="$1"
  shift
  if [[ "${STAGE1_NETWORK_ISOLATED:-0}" == "1" ]]; then
    (
      cd "$tmp"
      LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=UTC LEAN_PATH="$module_path" \
        "$lean_bin" "$@"
    )
  else
    bwrap --ro-bind / / --bind "$tmp" "$tmp" --dev /dev --proc /proc \
      --unshare-net --die-with-parent \
      --setenv LANG C.UTF-8 --setenv LC_ALL C.UTF-8 --setenv TZ UTC \
      --setenv LEAN_PATH "$module_path" --chdir "$tmp" "$lean_bin" "$@"
  fi
}

run_lean "$lean_path" --trust=0 -o Statement.olean Statement.lean >/dev/null
run_lean "$tmp:$lean_path" --trust=0 -o ObligationTree.olean ObligationTree.lean \
  > "$tmp/obligation.out"
run_lean "$tmp:$lean_path" --trust=0 Proof.lean > "$tmp/proof.out"
run_lean "$tmp:$lean_path" --trust=0 Validation.lean > "$tmp/validation.out"
cat "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out"

python3 -B - "$tmp/obligation.out" "$tmp/proof.out" "$tmp/validation.out" <<'PY'
import re
import sys
from pathlib import Path

obligation_output = Path(sys.argv[1]).read_text(encoding="utf-8")
proof_output = Path(sys.argv[2]).read_text(encoding="utf-8")
validation_output = Path(sys.argv[3]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
obligation_declarations = (
    "SimpleGraph.tutte",
    "Stage1Instances.THM_M_0856.ObligationTree.terminal_adapter",
    "Stage1Instances.THM_M_0856.ObligationTree.pinned_mathlib_terminal",
    "Stage1Instances.THM_M_0856.ObligationTree.compose_root",
)
proof_declarations = (
    "SimpleGraph.tutte",
    "Stage1Instances.THM_M_0856.Proof.pinnedTerminal",
    "Stage1Instances.THM_M_0856.Proof.tutteOneFactor_via_frozen_composition",
    "Stage1Instances.THM_M_0856.Proof.tutteOneFactor_direct",
)
validation_declarations = (
    "SimpleGraph.tutte",
    "Stage1Instances.THM_M_0856.Validation.tutteOneFactor_differential",
)


def observed_axioms(output: str, declaration: str) -> set[str]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    return {name.strip() for name in match.group(1).split(",") if name.strip()}


for declaration in obligation_declarations:
    assert observed_axioms(obligation_output, declaration) == allowed, declaration
for declaration in proof_declarations:
    assert observed_axioms(proof_output, declaration) == allowed, declaration
for declaration in validation_declarations:
    assert observed_axioms(validation_output, declaration) == allowed, declaration
assert proof_output.count("Declarations are sorry-free!") == len(proof_declarations)
assert validation_output.count("Declarations are sorry-free!") == len(validation_declarations)
combined = obligation_output + proof_output + validation_output
assert "sorryAx" not in combined
assert "declaration uses 'sorry'" not in combined
assert "error:" not in combined
PY
