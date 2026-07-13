# THM-M-0819 obligation architecture

Item: `S56-M-0819-OBLIGATION_TREE`

This is a frozen proof plan, not a completed proof. The exact root is Dilworth's primary
arbitrary-poset finite-width theorem from `Statement.lean`. Registry version 1 separates the
checked `k = 0` extension from the substantive positive-width theorem, expands the visible finite
proof opening, and makes the proposed finite-to-global compactness route explicit. No exact Lean
proof candidate or accepted terminal body is credited.

## Proof Route

The checked Lean harness consumes an abstract positive-width package. At `k = 0`, dependence of
every singleton forces the carrier empty and the zero-indexed family is a decomposition. At
positive width, fix the attained finite `k`-antichain `A`. For each requested finite set `s`, the
planned route applies finite Dilworth to the finite witness closure `s union A`, restricts its
`Fin k` coloring back to `s`, applies Rado selection, and turns global color fibers back into chains
with unique membership. This avoids claiming that an arbitrary finite `s` itself contains an exact
`k`-antichain. `M0819-L-FINITE-EXACTNESS` owns witness transport and final nonempty-fiber
compatibility; nonemptiness is source information, not an extra formal conclusion.

Only pages 161-162 of the primary source were available to the predecessor audit. The visible
finite argument supplies the width induction, the `U_i/L_i/N_i` construction, and upper and dual
lower residual-width lemmas. Its missing continuation is the explicit high-risk
`M0819-X-FINITE-TAIL` boundary, not an invented proof step.

`Finset.rado_selection_subtype` is present in pinned mathlib, but anchor inventory version 1 did not
classify it. It is therefore an open bridge with a mandatory append-only successor provenance audit,
not inherited proof credit. The external `minChainPartition_eq_antichainWidth` candidate remains a
finite, nonexact, current-pin-failing research lead.

## Typed Boundaries

- Proof edges run from a parent to each required child. Reverse `composes` edges exist only for the
  checked width-branch and root harness; every deeper reverse proof edge is navigational `refines`
  and its separate composition plan remains unverified.
- Refinement, provenance, evidence, trust, documentation, and workflow edges live in distinct graph
  indexes. No assurance overlay is a mathematical premise.
- Every proof nonleaf is marked `split-required`; every current proof leaf has an integer budget at
  most 100 and a structured open ledger. High-risk finite, compactness, and fiber-assembly nodes
  expose substantive planned transitions. Planned steps remain nonaccepted architecture and do not
  establish `R0` or kernel closure.
- This obligation-tree item implements generic `T01`-`T03`: registry freeze, typed graphs, and
  semantic expansion. The twelve open internal composition plans remain downstream proof/C01 work;
  none is represented as `composes` or parent closure.
- Accepted closed obligations and accepted receipt IDs are empty. The root remains `[H1, M3, R3]`.

## Node Index

The following anchors are stable public targets for registry nodes. Each short entry states the
local responsibility and its boundary; the complete typed fields and ledgers are authoritative in
`typed-graphs.json`.

<a id="m0819-root"></a>
### m0819-root
Exact arbitrary-poset finite-width Dilworth target. It remains open because the positive-width
child has no proof body.

<a id="m0819-s-definitions"></a>
### m0819-s-definitions
Owns exact cardinality, dependence, antichain, chain, and unique-membership decomposition bodies.

<a id="m0819-s-domain"></a>
### m0819-s-domain
Retains an arbitrary carrier and rejects a silent finite-poset specialization.

<a id="m0819-s-transport"></a>
### m0819-s-transport
Owns only the checked direct unfolding Iff; no finite-equality transport is credited.

<a id="m0819-s-foundation"></a>
### m0819-s-foundation
Requires the final classical, compactness, axiom, executable, olean, and no-oracle trust audit.

<a id="m0819-n-finite-restriction"></a>
### m0819-n-finite-restriction
Must transport order and width hypotheses exactly to every finite induced subtype.

<a id="m0819-n-coloring"></a>
### m0819-n-coloring
Must prove the bidirectional partition/coloring representation used by compactness.

<a id="m0819-b-width-zero"></a>
### m0819-b-width-zero
The local zero-width theorem is checked, but receives no accepted proof-state credit in this phase.

<a id="m0819-b-width-positive"></a>
### m0819-b-width-positive
The central open package matching the printed positive-width theorem.

<a id="m0819-c-local-colorings"></a>
### m0819-c-local-colorings
Chooses one exact local `Fin k` coloring for every finite restriction after finite Dilworth.

<a id="m0819-l-finite-dilworth"></a>
### m0819-l-finite-dilworth
The finite theorem is a major open bridge and cannot be hidden behind one invocation.

<a id="m0819-b-finite-induction"></a>
### m0819-b-finite-induction
Owns the inspected width-induction skeleton and its uninspected continuation.

<a id="m0819-c-adjoin-element"></a>
### m0819-c-adjoin-element
Constructs the source's chain decomposition after removing `a` and the `U_i/L_i/N_i` sets.

<a id="m0819-l-low-width-index"></a>
### m0819-l-low-width-index
Formalizes the inspected upper residual-width contradiction.

<a id="m0819-l-dual-index"></a>
### m0819-l-dual-index
Formalizes the source's dual lower residual-width step with an explicit order-dual transport.

<a id="m0819-x-finite-tail"></a>
### m0819-x-finite-tail
Blocks invented source mapping until the finite proof continuation is lawfully obtained and audited.

<a id="m0819-l-finite-exactness"></a>
### m0819-l-finite-exactness
Accounts for the attained `k`-antichain and prevents an at-most-`k` weakening from dropping it.

<a id="m0819-l-rado-selection"></a>
### m0819-l-rado-selection
The pinned compactness bridge is identified but requires a successor anchor/provenance audit.

<a id="m0819-c-global-coloring"></a>
### m0819-c-global-coloring
Constructs the global `Fin k` coloring returned by Rado selection.

<a id="m0819-l-global-proper"></a>
### m0819-l-global-proper
Uses two-point finite agreement to make equal-color elements comparable.

<a id="m0819-c-color-classes"></a>
### m0819-c-color-classes
Defines the candidate chain family as global coloring fibers.

<a id="m0819-l-fibers-chain"></a>
### m0819-l-fibers-chain
Turns same-color comparability into the exact `IsChain` conjunct.

<a id="m0819-l-unique-membership"></a>
### m0819-l-unique-membership
Proves every carrier element belongs to exactly its own color fiber.

<a id="m0819-t-positive-assemble"></a>
### m0819-t-positive-assemble
Must compose every finite-to-global child into the open positive-width package.

<a id="m0819-t-width-branches"></a>
### m0819-t-width-branches
The abstract positive and zero packages bundle by a checked term; the positive child stays open.

<a id="m0819-t-root-assemble"></a>
### m0819-t-root-assemble
The checked conditional branch-to-expanded-to-root composition, not a root proof body.

<a id="m0819-x-primary-source"></a>
### m0819-x-primary-source
Requires complete source pages, assumptions, errata status, node mapping, and independent H0 review.

<a id="m0819-x-finite-candidate"></a>
### m0819-x-finite-candidate
Records the finite ENat equality only as nonexact, unintegrated, current-pin-failing research input.

<a id="m0819-x-rado-provenance"></a>
### m0819-x-rado-provenance
Requires an append-only successor anchor inventory for the newly identified compactness bridge.

<a id="m0819-x-provenance"></a>
### m0819-x-provenance
Owns terminal-body origins, dependency hashes, licenses, wrappers, aliases, and revocations.

<a id="m0819-x-trust"></a>
### m0819-x-trust
Owns transitive declarations, axioms, compiled artifacts, executables, and independent replay.

<a id="m0819-x-readable"></a>
### m0819-x-readable
Requires a complete independently reviewed reconstruction; this architecture note is not `R0`.

<a id="m0819-x-workflow"></a>
### m0819-x-workflow
Keeps proof, validation, release, freshness, revocation, and master acceptance dependency-legal.

## Freeze Boundary

The registry freezes 33 obligations before proof status. The checked harness reports no recovery
holes and only `propext` where the zero-width proof uses set membership/extensionality machinery.
The substantive `PositiveWidthPackage` remains an explicit premise for which no inhabitant is
supplied or credited. There is no accepted H0,
M0, R0, audit completion, release evidence, theorem completion, or master acceptance. The single
positive-width cut is explicitly a coarse interface separator; `typed-graphs.json` also records the
deeper open semantic frontier.
