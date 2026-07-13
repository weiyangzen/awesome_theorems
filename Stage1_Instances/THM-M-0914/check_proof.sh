#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0914"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/stage1-m0914-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp/"

lean_path="$(cd "$lean_root" && lake env printenv LEAN_PATH)"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Fintype/Pigeonhole.olean"
test -f "$lean_root/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib/Data/Finset/Card.olean"

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
namespace = "Stage1Instances.THM_M_0914.Proof."
declarations = (
    "Finset.card_le_card_of_injOn",
    "Finset.exists_ne_map_eq_of_card_lt_of_maps_to",
    "Fintype.exists_ne_map_eq_of_card_lt",
    namespace + "cardInjOnBound_pinned",
    namespace + "finsetCollision_pinned",
    namespace + "finsetCollision_from_frozen_children",
    namespace + "fintypeWrapper_pinned",
    namespace + "fintypeWrapper_from_frozen_children",
    namespace + "root_via_pinned_wrapper",
    namespace + "root_via_frozen_children",
    namespace + "pigeonholeTarget_proof",
    namespace + "pigeonholeTarget_via_frozen_children",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"

assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "error:" not in output
print(
    "PASS THM-M-0914 Lean proof: 12 declarations sorry-free; "
    "axioms exactly propext, Classical.choice, Quot.sound"
)
PY
