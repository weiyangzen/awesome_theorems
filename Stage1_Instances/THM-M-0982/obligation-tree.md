# THM-M-0982 obligation tree

This version freezes eleven canonical obligations before proof-phase acceptance. Typed proof edges
run from a parent requirement to its child premise, with reciprocal `composes` edges. Source,
provenance, trust, documentation, and workflow edges never supply mathematical premises.

## M0982-ROOT

The exact conjunction has two proof children: `M0982-B-BELOW` and `M0982-B-ABOVE`.
`target_of_branches` checks their exact conjunction but is conditional, so the root remains `M3`.

## M0982-B-BELOW

Continuity from below consumes the pinned `tendsto_measure_iUnion_atTop` anchor. Mathlib's theorem is
stronger than the selected branch because it does not require the branch's measurable-event premise.

## M0982-B-ABOVE

Continuity from above consumes three independently visible obligations: the pinned intersection
anchor, measurable-to-null-measurable transport, and probability-measure finiteness at index zero.

## M0982-L-BELOW-ANCHOR

Terminal body: pinned mathlib `MeasureTheory.tendsto_measure_iUnion_atTop`. The obligation registry
does not treat the local wrapper as a second proof body.

## M0982-L-ABOVE-ANCHOR

Terminal body: pinned mathlib `MeasureTheory.tendsto_measure_iInter_atTop`. Its null-measurability
and finite-member premises are explicit siblings rather than hidden wrapper details.

## M0982-T-NULL

`measurable_to_nullMeasurable` checks the premise transport using
`MeasurableSet.nullMeasurableSet`.

## M0982-L-FINITE

`probability_member_ne_top` checks the required finite member via `measure_ne_top`.

## M0982-S-BOUNDARY

The statement-phase constant, empty-union, and universal-intersection probes retain the intended
degenerate cases. They constrain the encoding but do not prove either continuity branch.

## M0982-S-FOUNDATION

The transitive axiom and trusted-computing-base review remains a release-critical certificate.

## M0982-X-SOURCE

Pinpoint edition, theorem/page, premise, convention, and errata mapping remains open. This node has
no machine-proof eligibility and cannot be used as a proof premise.

## M0982-X-PROVENANCE

This informational overlay binds wrappers to the two terminal mathlib bodies and immutable anchor
audit. It prevents duplicate proof credit and does not affect machine closure.

## Status boundary

The registry and typed architecture are self-tested pending master acceptance. Proof integration,
human-source acceptance, readable reconstruction, hermetic validation, and theorem completion are
not claimed.
