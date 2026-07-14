#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "$0")/../.." && pwd)
target="$repo_root/Stage1_Instances/THM-M-0559"
lean_root="$repo_root/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-0559-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT

mkdir -p "$tmp/Stage1_Instances/THM-M-0559"
cp "$target/Statement.lean" "$tmp/Stage1_Instances/THM-M-0559/Statement.lean"
cp "$target/Proof.lean" "$tmp/Stage1_Instances/THM-M-0559/Proof.lean"

cd "$lean_root"
LEAN_NUM_THREADS=1 timeout 300 lake env lean --trust=0 -t0 -R "$tmp" \
  -o "$tmp/Stage1_Instances/THM-M-0559/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-0559/Statement.lean" > "$tmp/statement.out"
lean_path=$(lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 lake env lean --trust=0 -t0 -R "$tmp" \
  "$tmp/Stage1_Instances/THM-M-0559/Proof.lean" | tee "$tmp/proof.out"

python3 - "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
declarations = (
    "Stage1Instances.THM_M_0559.Proof.joined_of_component_eq",
    "Stage1Instances.THM_M_0559.Proof.exists_preimage_joined",
    "Stage1Instances.THM_M_0559.Proof.joined_of_map_joined",
    "Stage1Instances.THM_M_0559.Proof.components_surjective_iff",
    "Stage1Instances.THM_M_0559.Proof.components_injective_iff",
    "Stage1Instances.THM_M_0559.Proof.components_bijective_iff",
    "Stage1Instances.THM_M_0559.Proof.nonempty_zerothHomotopy_iff",
    "Stage1Instances.THM_M_0559.Proof.nonempty_iff_of_components_bijective",
    "Stage1Instances.THM_M_0559.Proof.empty_branch",
)
for declaration in declarations:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",") if name.strip()}
    assert actual == allowed, f"unexpected axioms for {declaration}: {actual}"
assert output.count("Declarations are sorry-free!") == len(declarations)
assert "sorryAx" not in output
assert "error:" not in output
print("PASS THM-M-0559 isolated Lean replay: component package and empty branch checked")
PY
