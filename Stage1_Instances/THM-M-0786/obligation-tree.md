# THM-M-0786 frozen obligation architecture

Item `S56-M-0786-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes in `obligation-registry.json`.
The 14 stable IDs are the later machine, human-source, and readable coverage
denominator. Any correction, split, merge, or eligibility change requires a
new registry version and an append-only delta.

## Proof route

The bounded anchor audit found an arbitrary-move Borel-determinacy theorem in
the immutable external source revision `42bc874b2357ca7e7573b31854a0d09761e11e41`.
The selected route constructs its full pruned Nat-move game for each canonical
payoff, transports the Borel predicate, relates legal-position strategies to
the canonical total-history strategies, preserves both winner branches and
the complement convention, and applies the external theorem. A final adapter
produces `PayoffSolver`; `root_of_payoffSolver` checks that this interface
assembles the exact canonical root.

This route does not claim knowledge of the external theorem's internal proof
tree. That source has not been materialized or kernel-audited in this pinned
environment. Its internal mathematical decomposition must be added by a
versioned registry delta after parser/elaborator-aware provenance and source
inspection, rather than invented here.

## Typed boundaries

`typed-graphs.json` keeps reciprocal proof requirement/composition edges apart
from refinement, source evidence, provenance, trust, documentation, and
workflow edges. Every node has an explicit input/output ledger and a semantic
step budget no larger than 100. `validation-specs.json` assigns one provisional
or open validation recipe to every frozen obligation.

## Status boundary

Only the existing statement encoding and conditional final composition have
scoped elaboration evidence. `root_of_payoffSolver` assumes the complete
substantive payoff solver and returns it at the definitionally equal root; it
earns no proof credit. The first open cut includes the Borel and strategy
transports, winner branch, full-game construction, external theorem kernel
integration, source map, trust closure, and provenance. The root remains
`[H1, M3, R3]`; audit and theorem completion are false.
