# THM-M-1009 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Erdos-Renyi second
lemma, understood provisionally as the generalized Borel-Cantelli lower bound.
It does not inherit proof credit from the legacy `S1_M_289.lean` artifact or
from the source metadata label `verified`.

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

The intended proof architecture starts with the finite event count, its first
and second moments, a second-moment lower bound, passage to tail unions, and a
limsup limit argument. This is a scope map, not a frozen obligation registry.
That registry belongs to the dependent obligation-tree phase.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate: no normalized expression
hash, environment fingerprint, checked transports, or mutation results exist.
The primary-source pinpoint and nomenclature audit is also open. The theorem is
not complete.

## Validation

The exact intake-only commands and results are recorded in `validation.md`.
They establish target membership, standard consistency, JSON syntax, and
dossier hygiene only. No Lean proof or kernel closure is claimed.
