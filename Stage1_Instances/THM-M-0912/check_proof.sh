#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0912"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0912-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Nat/Choose/Basic.olean"

cd "$tmp"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$lean_path" \
  lake env lean -o Statement.olean Statement.lean >/dev/null
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH=".:$lean_path" \
  lake env lean -o ObligationTree.olean ObligationTree.lean >/dev/null
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH=".:$lean_path" \
  lake env lean Proof.lean | tee proof.out

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
namespace = "Stage1Instances.THM_M_0912.Proof."
local_declarations = (
    "positiveColumnReindex_proof",
    "chooseSuccRight_proof",
    "predecessorRecurrence_from_frozen_children",
    "predecessorRecurrence_pinned",
    "root_via_pinned_composition",
    "root_via_frozen_children",
    "pascalIdentityTarget_proof",
    "pascalIdentityTarget_via_frozen_children",
)
declarations = (
    "Nat.choose_succ_right",
    "Nat.choose_eq_choose_pred_add",
) + tuple(namespace + name for name in local_declarations)

for declaration in declarations:
    marker = f"'{declaration}' does not depend on any axioms"
    assert marker not in output, f"expected propext axiom report for {declaration}"
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == {"propext"}, f"unexpected axiom closure for {declaration}: {actual}"

assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "error:" not in output
print("PASS THM-M-0912 Lean proof: 10 declarations sorry-free; axioms limited to propext")
PY
