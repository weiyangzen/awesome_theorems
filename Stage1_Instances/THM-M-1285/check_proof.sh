#!/usr/bin/env bash
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
TARGET="$ROOT/Stage1_Instances/THM-M-1285"
LEAN_ROOT="$ROOT/Formalizations/Lean"
TMP=$(mktemp -d /tmp/thm-m-1285-proof.XXXXXX)
trap 'rm -rf "$TMP"' EXIT

BASE=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)

cd "$LEAN_ROOT"
LEAN_NUM_THREADS=1 timeout --foreground 300 \
  lake env lean --trust=0 -t0 -R "$TARGET" \
  -o "$TMP/Statement.olean" "$TARGET/Statement.lean" \
  > "$TMP/statement.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout --foreground 300 \
  lake env lean --trust=0 -t0 -R "$TARGET" \
  -o "$TMP/ObligationTree.olean" "$TARGET/ObligationTree.lean" \
  > "$TMP/obligation-tree.out"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout --foreground 420 \
  lake env lean --trust=0 -t0 -R "$TARGET" \
  -o "$TMP/Proof.olean" "$TARGET/Proof.lean" \
  > "$TMP/proof.out"

python3 - "$TMP/proof.out" "$TMP/obligation-tree.out" <<'PY'
import re
import sys
from pathlib import Path

output = Path(sys.argv[1]).read_text(encoding="utf-8")
obligation_output = Path(sys.argv[2]).read_text(encoding="utf-8")
allowed = {"propext", "Classical.choice", "Quot.sound"}
proof_declarations = (
    "Stage1Instances.THM_M_1285.isRadial_profile",
    "Stage1Instances.THM_M_1285.isRadiallyNonincreasing_profile",
    "Stage1Instances.THM_M_1285.measurable_profile",
    "Stage1Instances.THM_M_1285.distribution_antitone",
    "Stage1Instances.THM_M_1285.iUnion_strictSuperlevel_gt",
    "Stage1Instances.THM_M_1285.distribution_iSup_rat_gt",
    "Stage1Instances.THM_M_1285.volume_ball_radiusForVolume",
    "Stage1Instances.THM_M_1285.radiusForVolume_mono",
    "Stage1Instances.THM_M_1285.starProfile_measurable",
    "Stage1Instances.THM_M_1285.starProfile_antitone",
    "Stage1Instances.THM_M_1285.strictSuperlevel_starProfile",
    "Stage1Instances.THM_M_1285.measure_strictSuperlevel_starProfile",
    "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_proof",
)
for declaration, report in [
    *((declaration, output) for declaration in proof_declarations),
    (
        "Stage1Instances.THM_M_1285.schwarzRearrangementTarget_of_construction",
        obligation_output,
    ),
]:
    match = re.search(
        re.escape(f"'{declaration}' depends on axioms: [") + r"(.*?)]",
        report,
        re.DOTALL,
    )
    assert match, f"missing axiom report for {declaration}"
    actual = {name.strip() for name in match.group(1).split(",")}
    assert actual == allowed, f"unexpected axiom closure for {declaration}: {actual}"
assert "sorryAx" not in output
PY

cat "$TMP/proof.out"

test -s "$TMP/Statement.olean"
test -s "$TMP/ObligationTree.olean"
test -s "$TMP/Proof.olean"
printf 'PROOF_SOURCE_SHA256='
sha256sum "$TARGET/Proof.lean" | cut -d' ' -f1
printf 'PROOF_OLEAN_SHA256='
sha256sum "$TMP/Proof.olean" | cut -d' ' -f1
printf 'PROOF_OUTPUT_SHA256='
sha256sum "$TMP/proof.out" | cut -d' ' -f1
echo "PASS THM-M-1285 isolated proof elaboration"
