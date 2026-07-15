#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
target="$repo_root/Stage1_Instances/THM-M-0321"
lean_root="$repo_root/Formalizations/Lean"
tmp="$(mktemp -d /tmp/thm-m-0321-proof.XXXXXX)"
trap 'rm -rf "$tmp"' EXIT

tmp_target="$tmp/Stage1_Instances/THM-M-0321"
mkdir -p "$tmp_target"
cp "$target"/{Statement,ObligationTree,Proof}.lean "$tmp_target/"

lean_bin="$(cd "$lean_root" && timeout 300 lake env which lean)"
lean_path="$(cd "$lean_root" && env -u LEAN_PATH timeout 300 lake env printenv LEAN_PATH)"

LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$tmp" \
  -o "$tmp_target/Statement.olean" "$tmp_target/Statement.lean" \
  >"$tmp/statement.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$tmp" \
  -o "$tmp_target/ObligationTree.olean" "$tmp_target/ObligationTree.lean" \
  >"$tmp/obligation-tree.out" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 \
  "$lean_bin" --trust=0 -t0 -R "$tmp" \
  "$tmp_target/Proof.lean" >"$tmp/proof.out" 2>&1

cat "$tmp/obligation-tree.out" "$tmp/proof.out"

python3 - "$tmp/obligation-tree.out" "$tmp/proof.out" <<'PY'
import re
import sys
from pathlib import Path

output = "\n".join(Path(path).read_text(encoding="utf-8") for path in sys.argv[1:])
declarations = (
    "Stage1Instances.THM_M_0321.ObligationTree.root_compose",
    "Stage1Instances.THM_M_0321.isClosed_fixedSetWithin",
    "Stage1Instances.THM_M_0321.isCompact_fixedSetWithin",
    "Stage1Instances.THM_M_0321.convex_fixedSetWithin",
    "Stage1Instances.THM_M_0321.mapsTo_fixedSetWithin_of_commute",
    "Stage1Instances.THM_M_0321.continuousOn_fixedSetWithin",
    "Stage1Instances.THM_M_0321.isAffineOn_fixedSetWithin",
    "Stage1Instances.THM_M_0321.cesaroAverage_mem",
    "Stage1Instances.THM_M_0321.affine_centerMass",
    "Stage1Instances.THM_M_0321.map_cesaroAverage",
    "Stage1Instances.THM_M_0321.cesaro_defect_eq",
    "Stage1Instances.THM_M_0321.tendsto_cesaro_defect_zero",
    "Stage1Instances.THM_M_0321.singleMap_fixedPoint",
    "Stage1Instances.THM_M_0321.isClosed_commonFixedSet",
    "Stage1Instances.THM_M_0321.isCompact_commonFixedSet",
    "Stage1Instances.THM_M_0321.convex_commonFixedSet",
    "Stage1Instances.THM_M_0321.mapsTo_commonFixedSet_of_commute",
    "Stage1Instances.THM_M_0321.finiteFamilyStep",
    "Stage1Instances.THM_M_0321.continuousCompactnessUpgrade",
    "Stage1Instances.THM_M_0321.markovKakutani_of_finiteFamily",
    "Stage1Instances.THM_M_0321.markovKakutani_proof",
)
allowed = {"propext", "Classical.choice", "Quot.sound"}
for declaration in declarations:
    report = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        output,
        re.DOTALL,
    )
    no_axioms = f"'{declaration}' does not depend on any axioms" in output
    assert report or no_axioms, f"missing axiom report for {declaration}"
    if report:
        actual = {part.strip() for part in report.group(1).split(",") if part.strip()}
        assert actual <= allowed, f"unexpected axioms for {declaration}: {actual}"
assert "sorryAx" not in output
assert "declaration uses 'sorry'" not in output
assert "error:" not in output
PY

if rg -n --pcre2 \
    '\b(?:sorry|admit|sorryAx|implemented_by|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe|extern)[[:space:]]' \
    "$target"/{Statement,ObligationTree,Proof}.lean; then
  echo "proof replay failed: prohibited proof device" >&2
  exit 1
fi

printf '%s\n' \
  'PASS THM-M-0321 proof: exact MarkovKakutaniTarget root checked' \
  'root kernel closure: provisional worker evidence; master acceptance pending'
