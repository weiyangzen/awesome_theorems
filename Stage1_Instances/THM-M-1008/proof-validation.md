# THM-M-1008 proof validation

Item: `S56-M-1008-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

`Proof.lean` proves the exact frozen `HewittSavageZeroOneTarget`. The proof approximates the
measurable path event by an initial cylinder, swaps its finite coordinate block with a disjoint
block, applies finite-block independence and iid reindexing, and lets the symmetric-difference
error tend to zero. The resulting real probability is idempotent, hence zero or one; the final
transport returns the required `ENNReal` conclusion. There are no placeholders or added axioms.

Validation reused the existing pinned Lake artifacts. No dependency update, fetch, clone, or build
command was run.

```text
BASE_LEAN_PATH=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
LEAN=$(cd Formalizations/Lean && lake env printenv LEAN)
TMP=$(mktemp -d /tmp/m1008-selftest.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_PATH="$BASE_LEAN_PATH" "$LEAN" -t 0 -o "$TMP/Statement.olean" \
  Stage1_Instances/THM-M-1008/Statement.lean
LEAN_PATH="$TMP:$BASE_LEAN_PATH" "$LEAN" -t 0 -o "$TMP/ObligationTree.olean" \
  Stage1_Instances/THM-M-1008/ObligationTree.lean
LEAN_PATH="$TMP:$BASE_LEAN_PATH" "$LEAN" -t 0 \
  Stage1_Instances/THM-M-1008/Proof.lean
  exit 0
  Stage1Instances.THM_M_1008.hewittSavageZeroOneTarget depends on axioms:
    [propext, Classical.choice, Quot.sound]

rg -n '(sorry|admit|axiom |sorryAx|placeholder|unsafe|implemented_by)' \
  Stage1_Instances/THM-M-1008 -g '*.lean'
  exit 1 (no matches)

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1008
  exit 0: rank 288, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1008/check_obligation_tree.py
  exit 0: 15 obligations and 30 typed edges passed
git diff --check -- Stage1_Instances/THM-M-1008 .stage1-worker-selftest.json
  exit 0
```

The proof phase is self-tested and pending master acceptance. This receipt does not claim the later
validation or release phases, audit completion, or theorem completion under all rev-5.6 gates.
