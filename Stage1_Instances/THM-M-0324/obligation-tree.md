# THM-M-0324 frozen obligation architecture

Item `S56-M-0324-OBLIGATION_TREE` freezes registry version 1 against the exact
`Statement.lean` and `anchor-audit.json` hashes recorded in
`obligation-registry.json`. Its 15 stable IDs are the denominator for later
machine, human-source, and readable coverage. Later proof discovery cannot
silently shrink the denominator; any split, merge, correction, exclusion, or
eligibility change requires an append-only versioned delta.

## Proof architecture

The selected route constructs Enflo's separable infinite-dimensional real
Banach space and excludes a Schauder basis through the approximation property.
The approximation-property definition is deliberately its own open obligation:
the exact source topology and finite-rank approximation convention must be
selected only after primary-source theorem-text review. Failure of that exact
property and the bridge from a Schauder basis to it are separate obligations.
The latter expands the apparently short library step into the finite-rank and
convergence facts for Schauder partial-sum projections.

The terminal contradiction is checked parametrically in `ObligationTree.lean`:
failure of a proposition `P`, together with a map from any Schauder basis to
`P`, excludes every basis. The final existential constructor separately checks
that a bundled Banach witness, infinite-dimensionality, separability, and the
no-basis result compose to the exact root. These small checked terms validate
only composition; they provide no Enflo construction or analytic premise.

## Typed graphs

`typed-graphs.json` stores reciprocal `proof_requires` and `composes` edges and
keeps refinement, source evidence, provenance, trust, documentation, and
workflow relations in separate graphs. Every node has the full rev-5.6 schema,
a substantive semantic ledger, and a step budget no greater than 100.
`validation-specs.json` binds one structured recipe to every obligation.

## Boundary

The root remains `M3` and theorem completion is false. The first open cut is
the exact approximation-property definition, construction of Enflo's space,
primary-source node mapping, and foundation audit. The existing source audit
is only `H1`; it does not authorize inventing the stronger approximation-
property statement. No obligation-tree receipt is accepted until the master
rechecks this provisional worker packet.
