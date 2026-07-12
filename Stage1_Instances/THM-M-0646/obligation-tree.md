# THM-M-0646 obligation registry and typed graphs

Registry version 1 freezes thirteen obligations before proof-phase closure is credited. Proof,
refinement, provenance, evidence, trust, documentation, and workflow are separate typed graphs.
Every proof edge has a reciprocal child-to-parent composition edge.

## root
The exact upward Loewenheim-Skolem target remains open at `M4` pending proof-node acceptance.

## s-exact
Preserve the frozen universes, ordered binders, infinitude assumption, all cardinal bounds, exact
cardinality, and elementary-equivalence conclusion.

## t-assemble
Compose the pinned equivalence interface into the root. The source-cardinality premise is retained
at the root but deliberately unused because the pinned theorem proves the stronger result.

## b-equiv
Convert the direction-dependent elementary embedding into elementary equivalence, reversing it in
the downward branch.

## c-card
Split on whether the requested cardinal is at most or greater than the source cardinal.

## b-down
Use downward Loewenheim-Skolem to construct a model of cardinality `kappa` elementarily embedding
into the source model.

## b-up
Build a large elementary-diagram model, shrink it to exact cardinality, reduce the expanded
language, and recover an elementary embedding from the source model.

## l-skolem
The imported downward elementary-substructure construction is a substantive terminal boundary,
not a leaf hidden by the short wrapper invocation.

## l-large
The imported large-model theorem for the elementary diagram is a substantive terminal boundary.

## l-diagram
The elementary-diagram model-to-embedding conversion is a separate construction invariant.

## x-pinned
Pin and deduplicate the eight distinct terminal bodies in mathlib revision `8a178386`; wrappers and
transports do not receive duplicate proof-body credit.

## x-source
A pinpoint primary source and independent human-source review remain open.

## x-tcb
Transitive kernel, dependency, executable, and axiom trust review remains open.

## Closure boundary

`ObligationTree.root_compose` checks the exact child-to-parent composition while accepting the
pinned elementary-equivalence route as an explicit premise. Consequently this phase records no
obligation closed. The proof phase's immediate machine cut set is `B-EQUIV`; the frozen proof graph
then exposes the direction split and its substantive imported construction boundaries. No `H0`,
accepted `M0-W`, `R0`, audit completion, or theorem completion is claimed.
