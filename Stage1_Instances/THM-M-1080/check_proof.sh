#!/usr/bin/env bash
set -euo pipefail

root="$(git rev-parse --show-toplevel)"
target="$root/Stage1_Instances/THM-M-1080"
lean_root="$root/Formalizations/Lean"
tmp="$(mktemp -d "${TMPDIR:-/tmp}/stage1-m1080-proof.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT

lean_bin="$(cd "$lean_root" && lake env which lean)"
base_lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"

test -x "$lean_bin"
test -n "$base_lean_path"
cp "$target"/{Statement,ObligationTree,Proof,ExactRoot}.lean "$tmp"/

run_lean() {
  local import_path="$1"
  shift
  (
    cd "$tmp"
    LEAN_NUM_THREADS=1 LEAN_PATH="$import_path" \
      timeout 1200s "$lean_bin" --trust=0 -t0 "$@"
  )
}

check_module() {
  local label="$1"
  local output="$2"
  shift 2
  if ! run_lean "$@" >"$output" 2>&1; then
    echo "FAIL: Lean rejected $label" >&2
    cat "$output" >&2
    exit 1
  fi
}

check_module "Statement.lean" "$tmp/statement.out" \
  "$base_lean_path" -o Statement.olean Statement.lean
check_module "ObligationTree.lean" "$tmp/obligation-tree.out" \
  "$tmp:$base_lean_path" -o ObligationTree.olean ObligationTree.lean
check_module "Proof.lean" "$tmp/proof.out" \
  "$base_lean_path" -o Proof.olean Proof.lean
check_module "ExactRoot.lean" "$tmp/exact-root.out" \
  "$tmp:$base_lean_path" -o ExactRoot.olean ExactRoot.lean

python3 - "$tmp/obligation-tree.out" "$tmp/proof.out" "$tmp/exact-root.out" <<'PY'
from pathlib import Path
import re
import sys

if not __debug__:
    raise SystemExit("FAIL: Python assertions are disabled")

allowed = {"propext", "Classical.choice", "Quot.sound"}
expected = {
    Path(sys.argv[1]): ["azumaUpperTail_of_threshold_packages"],
    Path(sys.argv[2]): [
        "sum_increment_eq_sub",
        "exp_secant_bound",
        "condExp_exp_increment_le",
        "exp_endpoint_integrable",
        "exp_increment_sum_integral_le",
        "positiveThreshold",
        "zeroThreshold",
        "azumaUpperTail",
    ],
    Path(sys.argv[3]): [
        "positiveThresholdPackage",
        "zeroThresholdPackage",
        "azumaUpperTail_exact",
    ],
}

for path, declarations in expected.items():
    output = path.read_text(encoding="utf-8")
    assert "error:" not in output, f"{path.name}: Lean error"
    assert "sorryAx" not in output, f"{path.name}: sorryAx in axiom closure"
    for declaration in declarations:
        match = re.search(
            rf"'[^']*\.{re.escape(declaration)}' depends on axioms: \[(.*?)]",
            output,
            re.DOTALL,
        )
        assert match, f"{path.name}: missing axiom report for {declaration}"
        actual = {item.strip() for item in match.group(1).split(",") if item.strip()}
        assert actual == allowed, (
            f"{path.name}: unexpected axioms for {declaration}: {sorted(actual)}"
        )

print("PASS THM-M-1080 Lean proof: exact frozen root and composition elaborate with --trust=0")
PY

if rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern)[[:space:]]' \
  "$target/Proof.lean" "$target/ExactRoot.lean"; then
  echo "FAIL: prohibited proof construct" >&2
  exit 1
fi

python3 -B "$target/check_proof.py"
