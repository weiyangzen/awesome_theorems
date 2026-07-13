# THM-M-1057 proof-phase validation

Item: `S56-M-1057-PROOF`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2`.

## Implemented Proof

Eight complete Apache-2.0 proof modules are vendored from
`marcmorningstar/lean4-ergodic-theory` at immutable commit
`ed3fa6b8a30594eeb791160563942ba115581aa0`. Their target-local import changes,
pinned API renames, two compatibility lemmas, exact upstream and port hashes,
and license are recorded in `PORT_PROVENANCE.md`.

The imported theorem expects a pointwise subadditive cocycle, while the frozen
target assumes each inequality only almost everywhere. `Proof.lean` forms a
measurable simultaneous good set using `aeSeqSet`, intersects all of its
forward-iterate preimages, and changes the transformation and process only off
that invariant full-measure set. The resulting process is pointwise
subadditive, integrable, and a.e. equal levelwise to the original. The vendored
means theorem and deterministic Fekete identification then construct the
frozen `PointwiseLimitPackage`; the pre-frozen composer yields the unchanged
exact root.

## Commands And Results

Validation uses only the existing pinned Lake environment. No `lake update`,
`lake build`, clone, fetch, network access, or `.lake` mutation is used.

```text
python3 Stage1_Instances/THM-M-1057/check_proof.py
  exit 0
  Reconstruct all eight immutable upstream sources, compile the complete stack
  in a fresh temporary directory with --trust=0, and check receipts, sorries,
  axioms, hashes, pins, and changed-path ownership.

python3 Stage1_Instances/THM-M-1057/check_obligation_tree.py
  exit 0
  Frozen 15-obligation denominator and 46 typed edges remain valid.

python3 Docs/tools/check_stage1_standard.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-1057
  exit 0 for all three preflight commands.

git diff --check -- Stage1_Instances/THM-M-1057 \
  .stage1-worker-selftest.json
  exit 0; no whitespace errors.
```

This is a provisional proof-phase `M0-P` proposal pending master acceptance,
not an authoritative state transition. The frozen definitions, boundary, and
foundation machine obligations remain open. The structured validation recipes
are still planned, and full transitive trust, source/readability acceptance,
hermetic replay, independent verification, validation, and release gates are
downstream. Neither audit completion nor theorem completion is claimed.
