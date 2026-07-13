# THM-M-1009 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Erdos-Renyi second
lemma, understood as the generalized Borel-Cantelli lower bound. The proof
phase now has a provisional worker-self-tested local body for the exact frozen
root. It does not inherit proof credit from the legacy `S1_M_289.lean`
artifact or from the source metadata label `verified`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | Lower bound for the measure of the limsup by the limsup of the finite second-moment ratio | Exact indexing, real/ENNReal encoding, elaboration, and expression fingerprint belong to the statement phase |
| Objects | Probability space, sequence of measurable events, finite single and double probability sums | Sigma-finiteness is supplied by the probability assumption; measurability and denominator behavior must be mutation-tested |
| Main hypothesis | Divergence of the event-probability partial sums | The precise `Tendsto` encoding is only a candidate |
| Primary conclusion | `limsup` ratio is at most the probability of infinitely many events | Direction, initial-segment convention, and conversion through `Measure.real` require source and statement checks |
| Corollary | Ratio tending to one implies the limsup event has probability one | Named alternate target only; no implication proof is credited |
| Nearby anchors | Independent second Borel-Cantelli and Levy generalized Borel-Cantelli | Strictly infrastructure, not closure of the generalized lower bound |
| Foundations | Lean 4 kernel and pinned mathlib | Version, dependency fingerprint, axioms, and TCB remain open |

`Proof.lean` realizes the frozen architecture through the finite event count,
its first and second moments, a finite Cauchy-Schwarz bound, shifted-window
tail estimates, a limsup comparison, and continuity from above.

## Intake verdict

Lifecycle remains `planned`, and the accepted root vector remains
`[H1, M3, R3]`. The proof worker proposes `M0-L` only after master acceptance
of its node receipt. The primary-source pinpoint, readable reconstruction,
validation, release, and theorem-completion gates remain open.

## Validation

Intake evidence remains in `validation.md`. Proof-phase commands, exact hashes,
axioms, and boundaries are recorded separately in `proof-validation.md` and
`proof-receipt.json`. No accepted theorem completion is claimed.
