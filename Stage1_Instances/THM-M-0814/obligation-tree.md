# THM-M-0814 frozen obligation architecture

Item `S56-M-0814-OBLIGATION_TREE` freezes registry version 1 against the exact statement and the
version-2 anchor audit. Its 33 canonical IDs form the later coverage denominator. Eligibility is
derived from the frozen theorem and the source proof's semantic work, not from which Lean candidates
were found. Any target correction, split, merge, exclusion, eligibility change, edge-role change,
or terminal-body identity change requires registry version 2 and an append-only delta.

## Checked proof spine {#m0814-root}

```text
M0814-ROOT exact max-flow/min-cut target [M3]
`-- M0814-T-ASSEMBLE conditional exact root assembly
    |-- M0814-L-MAX-ATTAIN maximum-flow attainment [open]
    `-- M0814-T-CUT-CERT conditional minimum-cut certificate
        |-- M0814-L-WEAK-DUALITY [open]
        `-- M0814-T-EQUAL-CUT [open]
```

`root_of_terminal`, `compose_root`, and `cutCertificate_compose` are exact conditional Lean
certificates. Every substantive child is an explicit argument and is consumed. No argument is
inhabited in this phase, so these declarations give no proof or closure credit.

### m0814-root

The root is the fully explicit `MaxFlowMinCutTarget` expression fingerprinted in the statement
phase. Its sole proof-spine child is the exact terminal assembly; assurance and readable overlays
remain separately typed and never act as proof premises.

### m0814-t-assemble

The terminal assembly takes an exact maximum-flow witness theorem and, for that selected flow, an
exact minimum-cut/equality theorem. It constructs every conjunct of
`MaxFlowMinCutTarget` without changing domains or adding assumptions.

### m0814-l-max-attain

This exact interface says every canonical network has a feasible flow whose value dominates every
feasible flow. The paper obtains it by finite chain coordinates and compact polytope maximization;
the interface itself is not a proof of compactness or attainment.

### m0814-t-cut-cert

`cutCertificate_compose` consumes exact weak duality and an equal disconnecting set for a selected
maximum flow. Rewriting by equality makes that set no more expensive than every disconnecting set.

### m0814-l-weak-duality

For an arbitrary feasible flow and disconnecting set, every supported chain contributes at least
once to the cut-side double sum, and each cut-arc load is capacity-bounded. Multiple crossings must
be handled without subtractive arithmetic or an illicit exactly-once assumption.

### m0814-t-equal-cut

The output of Ford and Fulkerson's three-lemma construction is kept separate from weak duality: for
any chosen maximum flow it constructs a disconnecting set with equal value. Its source-body
decomposition remains open.

## Statement Layer

### m0814-s-target

The exact target quantifies finite ambient vertex and arc types, an undirected `Graph V E`, distinct
terminals in the vertex set, and strictly positive `NNReal` capacities. It requires attained maximum
and minimum witnesses plus value equality.

### m0814-s-chain

`Chain` has positive length, injective dependent vertex and arc arrays, fixed endpoints, and
`Graph.IsLink` evidence. Finiteness and equality of these proof-bearing values are not obtained just
from finiteness of `V` and `E`; the normalization layer must construct a duplicate-free semantic
representation.

### m0814-s-flow-cut

Flows are `Chain G source sink ->₀ NNReal`; loads and values are finite `Finsupp.sum`s. A
disconnecting `Finset E` contains only graph arcs and meets every chain, not only positive supported
components. These definitions remain the only credited representation.

### m0814-s-boundary

No-chain and no-edge networks are included. The intended zero-flow/empty-cut witnesses must be
proved from the frozen definitions. Parallel arcs and isolated vertices remain in scope; loops are
inert for injective-vertex chains. No path-existence premise may be added.

### m0814-s-transport

Only `maxFlowMinCutTarget_iff_expanded` is checked. Directed conservation flows, vertex-partition
cuts, signed real flows, and other capacity domains remain uncredited transports.

### m0814-s-foundation

Finite enumeration, compactness, convex averaging, `NNReal` arithmetic, choice, proof irrelevance,
and quotient reasoning require a transitive axiom/import audit. No solver, native evaluation,
external oracle, or unchecked finite certificate is permitted or credited.

## Normalization And Branches

### m0814-n-chain-enum

Construct a finite duplicate-free coordinate index for all semantic chains, including the dependent
proof-field quotient or extensionality needed to avoid counting proof variants as different paths.

### m0814-n-flow-coord

Transport `Finsupp` flows to finite nonnegative coordinates and prove exact equations for component
sum and every arc load. This is a representation bridge, not a definitional simplification.

### m0814-b-no-chain

When no chain exists, prove zero flow feasible, empty set disconnecting, both universal extrema, and
zero equality. The branch is explicit because the source's averaging arguments assume a chain.

### m0814-b-has-chain

For a nonempty finite chain family, execute the maximum-flow and left-cut construction without
changing the canonical chain representation.

### m0814-b-merge

Prove the chain-existence split exhaustive and return the same canonical target from both branches.

## Source Proof Expansion

The following relations mirror printed pages 400-402. They are stored as reciprocal
`proof_requires` / `logical_decomposition` edges and explicit unverified plans, never as checked
`composes` edges. Each needs a future exact Lean child-to-parent certificate.

### m0814-c-feasible-polytope

Build the nonempty closed bounded coordinate region cut out by nonnegativity and every finite arc
capacity inequality. Prove the coordinate sum continuous and transport all facts back to `Flow`.

### m0814-l-max-convex

Show that the maximum-flow locus is convex. Given finitely many arcs and a maximum flow leaving each
one unsaturated, construct an average maximum flow with strict slack on every selected arc.

### m0814-c-saturated-core

Define `S` as exactly the graph arcs saturated in every maximum flow, with decidable finite
membership and the correct `arcLoad = capacity` predicate.

### m0814-l-s-disconnects

Source Lemma 1. If a chain avoids `S`, average maximum flows witnessing slack on its arcs, take a
positive minimum slack, and increase that chain component, contradicting maximality.

### m0814-l-reroute-basic

Formalize the paper's suppressed "chain contained in" steps: splice walks, erase loops to recover an
injective chain, update `Finsupp` weights without underflow, and prove nonnegativity, feasibility,
support behavior, and exact value preservation.

### m0814-l-s-orientation

If two positive component chains traverse an `S` arc oppositely, reroute them to unsaturate it while
preserving maximal value. Distinct-flow witnesses first pass through a convex average. This defines
a common left endpoint for every arc in `S`.

### m0814-c-left-arcs

Define `L` as the arcs in `S` whose left endpoint has a possibly empty source prefix all of whose
arcs are unsaturated by one maximum flow. Preserve the maximum-flow and prefix witnesses.

### m0814-l-l-disconnects

Source Lemma 2. On any source-to-sink chain, take its first `S` arc. Average slack witnesses for the
prefix, then reroute if the prefix reaches the wrong endpoint. The contradiction makes that arc a
member of `L`.

### m0814-l-l-at-most-one

Source Lemma 3. If a positive maximum-flow component contains two `L` arcs, average with the
leftness witness for the second and reroute the suffix. The first arc becomes unsaturated,
contradicting its membership in `S`.

### m0814-l-l-exactly-one

Every chain meets `L` because `L` disconnects; every positive component meets it at most once by
Lemma 3. Combine both facts to obtain exactly one crossing for each positive supported component.

### m0814-l-count-once

Each `L` arc is saturated by the selected maximum flow. Interchange the finite arc/component sums,
then use exactly-one crossing to show that summing capacities over `L` counts each positive chain
weight exactly once. This yields `flowValue flow = cutValue capacity L`.

## Assurance Boundaries

### m0814-x-source

The frozen architecture maps Ford and Fulkerson, *Maximal Flow Through a Network* (1956), Section 1
definitions on pages 399-400, Theorem 1 and Lemmas 1-3 on pages 400-402. Catalog identity, historical
"number" to `NNReal`, loop conventions, corrections/errata, every suppressed step, and independent
review remain open at `H1`.

### m0814-x-provenance

No exact root proof candidate was found. Every future local or imported terminal body, wrapper,
source slice, dependency, license, and transitive declaration origin must be content-addressed; the
Atlas and CLRS candidates remain nonexact support only.

### m0814-x-trust

The current conditional harness reports only `propext`, `Classical.choice`, and `Quot.sound` and is
explicitly sorry-free. Proof-specific transitive dependencies, imported oleans, executables, cold
offline replay, independent validation, and release trust remain open.

### m0814-x-readable

This architecture is not an independently reviewed readable proof. Every node has a substantive
ledger and a budget below 100, but every detailed inference and rerouting invariant must still be
reconstructed before `R0`.

### m0814-x-workflow

Proof implementation, validation, hermetic replay, independent verification, release, freshness,
revocation, and master acceptance remain separate workflow obligations and are never proof premises.

## Freeze Boundary

The canonical denominator has 33 obligations. Conditional interface checks close none of them, the
accepted closed set is empty, and the root remains `[H1, M3, R4]`. The predecessor statement and
anchor packets and this proposal await dependency-ordered master acceptance. Source `H0`, proof
`M0`, readable `R0`, `AUDIT-Z`, validation, release, and theorem completion are not claimed.
