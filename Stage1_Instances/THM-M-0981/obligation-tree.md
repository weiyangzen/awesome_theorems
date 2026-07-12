# THM-M-0981 frozen obligation architecture

Item: `S56-M-0981-OBLIGATION_TREE`.

Registry version 1 freezes 14 semantic obligations before the proof phase assigns any closure
credit. Eleven obligations are root-relevant machine obligations; provenance, human-source, and
TCB records are informational overlays. Availability of the three audited mathlib anchors does not
exclude them from the denominator and does not close them in this phase.

## Typed proof route

```text
M0981-ROOT exact KolmogorovAxiomsTarget [open M1]
`-- M0981-T-ASSEMBLE checked conditional composition
    `-- M0981-B-CLAUSES exhaustive conjunction split
        |-- M0981-L-EMPTY       P empty = 0
        |-- M0981-L-UNIT        P univ = 1
        |   `-- M0981-N-INSTANCE explicit premise to local instance
        `-- M0981-L-ADDITIVITY  measure of disjoint union = tsum
```

## root

`M0981-ROOT` is exactly the universe-polymorphic proposition fingerprinted in `statement.json`.
It quantifies over every measurable sample type and every measure with an explicit
`IsProbabilityMeasure` premise.

## s-exact

`M0981-S-EXACT` owns the exact binder order and the ordered empty-event, unit-mass, and countable-
additivity conjunction. It prevents replacing the target with only one clause or a subtype-only
formulation.

## s-boundary

`M0981-S-BOUNDARY` retains empty sample types and the empty event family. No nonemptiness,
positivity, or nonempty-family premise may be introduced.

## s-transport

`M0981-S-TRANSPORT` records the checked equivalence with `ProbabilityMeasure` subtype packaging.
It is a transport, not a second semantic obligation or a second proof body.

## s-foundation

`M0981-S-FOUNDATION` owns the accepted-axiom and no-oracle policy. The anchor probe observed
`propext`, `Classical.choice`, and `Quot.sound`; a complete transitive release audit remains open.

## n-instance

`M0981-N-INSTANCE` converts the target's explicit `IsProbabilityMeasure P` premise into the local
typeclass instance expected by `IsProbabilityMeasure.measure_univ`. It adds no assumption.

## b-clauses

`M0981-B-CLAUSES` is the exhaustive three-way conjunction decomposition. Its recomposition is
checked by `ObligationTree.root_compose`.

## l-empty

`M0981-L-EMPTY` is anchored to pinned `MeasureTheory.measure_empty`. The future proof phase must
integrate and validate its terminal-body provenance rather than credit its name alone.

## l-unit

`M0981-L-UNIT` is anchored to pinned `MeasureTheory.IsProbabilityMeasure.measure_univ` after the
explicit-to-instance normalization.

## l-additivity

`M0981-L-ADDITIVITY` is anchored to pinned `MeasureTheory.measure_iUnion` with exactly the target's
Nat-indexed measurability and pairwise-disjointness premises and conclusion orientation.

## t-assemble

`M0981-T-ASSEMBLE` is kernel-checked by `ObligationTree.root_compose`. It consumes three universal
clause packages and returns the canonical nested conjunction without invoking a measure theorem.
Its premises remain open here, so it is not an unconditional proof.

## x-provenance

`M0981-X-PROVENANCE` separates imported terminal bodies from local wrappers and transports. Full
transitive declaration and source-body resolution belongs to later proof and validation phases.

## x-source

`M0981-X-SOURCE` remains `H1`: primary-source edition, theorem/page, assumptions, errata, and
independent node review are not accepted by this architecture phase.

## x-tcb

`M0981-X-TCB` remains open for compiled-artifact, executable, dependency, axiom, offline replay,
and independent-runner evidence.

## Freeze boundary

The frozen root cut set is `M0981-L-EMPTY`, `M0981-L-UNIT`, and `M0981-L-ADDITIVITY`. Separate
refinement, proof, provenance, evidence, trust, documentation, and workflow graphs prevent source
or governance nodes from becoming proof premises. Every semantic ledger is under 100 steps.

This phase claims no accepted proof node, source review, readable reconstruction review, audit
completion, theorem completion, release readiness, or master acceptance. Any correction, split,
merge, exclusion, eligibility, weight, or risk change requires registry version 2 and an append-only
old/new ID delta.
