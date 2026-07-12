# THM-M-1054 proof-phase validation

Item: `S56-M-1054-PROOF`. Base revision:
`45ecc126e04773079f94f7b6f73d4f4c9a6da900`.

`Proof.lean` instantiates the frozen nontrivial package with the pinned
`ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection` theorem and
feeds that body to the checked subsingleton/nontrivial assembly. The resulting
declaration has exactly the intake-frozen `VonNeumannL2MeanErgodicTarget` type.
No assumptions were added and no theorem was broadened or substituted.

Validation ran in the worker clone on 2026-07-12. Existing pinned `.lake`
artifacts were reused; no update, build, clone, fetch, or `.lake` mutation was
performed.

## Commands and exact results

```text
$ python3 Docs/tools/check_stage1_standard.py
check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy
slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
exit 0

$ python3 scripts/stage1_target.py check
stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
exit 0

$ python3 scripts/stage1_target.py show THM-M-1054
rank 246; planned; hard_mathlib_anchor_and_wrapper; theorem_complete false
exit 0

$ cd Formalizations/Lean
$ tmp=$(mktemp -d ./.m1054-proof.XXXXXX); trap 'rm -rf "$tmp"' EXIT
$ cp ../../Stage1_Instances/THM-M-1054/{Statement,ObligationTree,Proof}.lean "$tmp/"
$ lake env lean -o "$tmp/Statement.olean" "$tmp/Statement.lean" && \
    LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean \
      -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean" && \
    LEAN_PATH="$tmp:$(lake env printenv LEAN_PATH)" lake env lean "$tmp/Proof.lean"
exit 0; exact target and all three modules elaborated. Lean reported for both
new proof declarations only [propext, Classical.choice, Quot.sound].

$ python3 Stage1_Instances/THM-M-1054/check_proof.py
PASS THM-M-1054 proof: pinned mean-ergodic body and exact root integrated
proof sha256: 40a65bc109a0fac7b96f9234cabe05312abb127f1883707499dc5fbcc05e43e1
machine root cut set after proof integration: empty; downstream gates remain
exit 0

$ python3 -m json.tool Stage1_Instances/THM-M-1054/proof-receipt.json >/dev/null
exit 0

$ rg -n 'sorry|admit|sorryAx|axiom |unsafe|native_decide|external ' \
    Stage1_Instances/THM-M-1054/Proof.lean
exit 1; no forbidden proof mechanism (no-match exit)

$ git diff --check -- Stage1_Instances/THM-M-1054 .stage1-worker-selftest.json
exit 0; no output
```

The proof-phase machine root cut set is empty. This is not theorem completion:
validation, provenance/trust closure, hermetic replay, independent verification,
human source and readable review, release, and master acceptance remain open.
