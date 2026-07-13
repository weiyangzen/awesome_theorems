# THM-M-1522 proof-phase validation

Item: `S56-M-1522-PROOF`. Base revision:
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`.

## Implemented bodies

The complete `MaximalErgodic.lean` and `Birkhoff.lean` proof modules are
vendored from Apache-2.0 project `marcmorningstar/lean4-ergodic-theory` at
commit `ed3fa6b8a30594eeb791160563942ba115581aa0`. The compatibility delta is
limited to the target-local sibling import and the pinned-mathlib spelling
`integrable_finset_sum`; both files carry prominent modification notices, and
the full upstream license and exact provenance are included.

`Proof.lean` uses the vendored general theorem to construct the frozen
`GeneralPointwiseLimitPackage`, with conditional expectation as its invariant
limit. It proves `ErgodicInvariantLimitIdentification` locally from ergodic
almost-everywhere constancy, probability normalization, and the stored integral
identity. The pre-proof composition declaration then yields the unchanged exact
root. A direct adapter to the vendored ergodic corollary independently confirms
the target type; both adapters share one terminal proof route and receive no
duplicate proof-body credit.

## Commands and results

Validation ran in this worker clone on 2026-07-14 using only the existing
pinned Lake environment. No update, build, clone, fetch, or mutation of
`.lake` was performed.

```text
python3 Stage1_Instances/THM-M-1522/check_proof.py
  exit 0
  Fresh trust-level-zero temporary elaboration passed for Statement,
  MaximalErgodic, Birkhoff, ObligationTree, and Proof.
  Three vendored terminal declarations and four local declarations are
  sorry-free and report [propext, Classical.choice, Quot.sound].

python3 Stage1_Instances/THM-M-1522/check_obligation_tree.py
  exit 0
  Frozen 16-obligation denominator, 32 typed edges, and conditional root
  composition remain valid.

python3 Docs/tools/check_stage1_standard.py
  exit 0
  15 assurance groups and 1546 uniform-L0 Lean 4 targets passed.

python3 scripts/stage1_target.py check
  exit 0
  1546 unique targets, ranks 1 through 1546, all L0/rework_required.

python3 scripts/stage1_target.py show THM-M-1522
  exit 0
  Rank 190, planned, L0/rework-required, theorem_complete=false.

python3 -m json.tool Stage1_Instances/THM-M-1522/proof-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for both files.

git diff --check -- Stage1_Instances/THM-M-1522 \
  .stage1-worker-selftest.json
  exit 0; no whitespace errors.
```

This is self-tested proof-node evidence with a provisional `M0-P` proposal,
pending master acceptance. The required foundation certificate and all later
validation, source/readability review, hermetic replay, independent verification,
and release gates remain open. Neither theorem completion nor an authoritative
state transition is claimed.
