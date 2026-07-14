# THM-M-1083 proof execution

Item: `S56-M-1083-PROOF`. Base revision:
`a1a7e939e58f103f5ff5d23af51437fa8658aa04`.

## Result

The exact canonical root is now kernel-closed through an alternate terminal route as a provisional
proof-phase `M0-P` candidate pending frozen-graph reconciliation and master acceptance.
`Proof.lean` constructs the dimension-one covering-number witness for the intrinsic interval,
translates the target moment bound into `IsKolmogorovProcess`, invokes the complete vendored
`ProbabilityTheory.exists_modification_holder` body, reverses its fixed-time equality, and converts
`HolderOnWith` on `univ` to the target's `HolderWith` path predicate.

The terminal theorem and its complete 15-file transitive Lean closure are vendored from immutable
`RemyDegenne/brownian-motion` commit
`91885e6172648ea7f9c6a16b3a7069f92c88e023` under Apache-2.0. Seven files have only local import
qualification; `PORT_PROVENANCE.md` records every upstream and adapted hash, and `check_proof.py`
inverts the adaptation to recover all upstream sources byte-for-byte.

## Evidence Boundary

The narrow replay builds every vendored module and `Statement.lean` into a disposable temporary
olean tree, then checks `Proof.lean` with `--trust=0 -t0`. The four local declarations report exactly
`propext`, `Classical.choice`, and `Quot.sound`. No dependency is updated, built, cloned, fetched, or
otherwise mutated; only the pre-existing pinned `.lake` artifacts are read.

This is an unaccepted worker proof proposal. The statement and boundary interfaces retain their
predecessor evidence. The vendored terminal body reaches the exact root through integrable supremum
bounds and dense extension rather than the frozen Markov/Borel-Cantelli route, so the internal graph
remains open pending integration-lane mapping, splitting, or supersession. `M1083-S-FOUNDATION`, full
transitive trust/provenance review, validation, hermetic replay, independent verification,
source/readability acceptance, release, `AUDIT-Z`, and `THEOREM-Z` remain downstream. Neither
accepted state nor theorem completion is claimed.
