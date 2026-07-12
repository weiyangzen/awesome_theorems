# Frozen obligation architecture

Item: `S56-M-0772-OBLIGATION_TREE`  
Registry: `THM-M-0772-OBLIGATIONS-v1`  
Freeze date: 2026-07-12 (Asia/Shanghai)

The registry was frozen from the exact statement and anchor inventory. It treats the short call to
`maxChain_spec` as a critical bridge with a separate imported-body and provenance boundary. Thus an
adapter cannot create duplicate semantic credit or conceal the construction behind a library name.

## M0772-ROOT

Exact target: every `P : Type u` carrying `PartialOrder P` admits a `c : Set P` satisfying
`IsMaxChain (fun x y => x <= y) c`. It requires the terminal adapter and remains `M3` here.

## M0772-S-DEFINITIONS

`IsChain` means pairwise comparability; `IsMaxChain` adds equality with every chain containing the
chosen set. Inclusion-maximality is not maximum cardinality and is not maximality of an element.

## M0772-S-DOMAIN

The carrier is universe-polymorphic and arbitrary. The only class assumption is `PartialOrder P`;
there is no `Nonempty`, finiteness, completeness, or cardinality premise.

## M0772-S-BOUNDARY

The existing `emptyBoundary` and `singletonBoundary` declarations kernel-check witnesses for the
two degenerate carriers. They constrain the architecture but do not prove the general root.

## M0772-S-EXPANDED

`hausdorffMaximalPrinciple_iff_expanded` checks both directions between the named predicate and its
chainhood-plus-inclusion expansion.

## M0772-S-FOUNDATION

Release must accept and reproduce the observed `[propext, Classical.choice, Quot.sound]` boundary,
the pinned Lean kernel, and the absence of undeclared axioms, oracles, and unsafe code transitively.

## M0772-N-RELATION

Specialize the imported relation variable to `fun x y => x <= y`. This is a normalization step,
not a changed theorem: it introduces no premise and yields the exact relation in the target.

## M0772-C-WITNESS

The existential witness is `maxChain (fun x y => x <= y)`. Its maximality is not inferred from the
name; it is consumed only from `M0772-L-MAXCHAIN`.

## M0772-L-MAXCHAIN

Bridge claim: every relation `r` has some `c` satisfying `IsMaxChain r c`. The pinned candidate is
the witness `maxChain r` with `Mathlib.Order.CompleteLattice.Chain.maxChain_spec`. This registry
records it as provisional `M0-W`, not accepted root closure.

## M0772-T-ADAPTER

`root_of_relationGenericMaxChain` is the checked composition certificate. It binds the bridge as an
abstract named hypothesis, specializes it, packages the witness, and returns the complete root.

## M0772-X-MATHLIB-BODY

This terminal boundary owns the actual `maxChain_spec` body at mathlib commit
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. A downstream proof/provenance phase must close its
transitive construction dependencies and bind immutable evidence before it can compose upward.

## M0772-X-PROVENANCE

This non-duplicating overlay owns transitive declaration hashes, imports, axioms, placeholder and
unsafe scans, TCB identity, license, and replay evidence. It cannot serve as a proof premise.

## M0772-X-SOURCE

Primary-source passages for the construction, chainhood, and maximality argument require an
independent human review. This node contributes H coverage only and cannot close machine debt.

## Graph and closure boundary

The seven separate graphs are `proof`, `refinement`, `provenance`, `evidence`, `trust`,
`documentation`, and `workflow`. Every proof requirement has an explicit reciprocal `composes`
edge. Governance, source, documentation, and trust edges never enter the proof graph.

The frozen root cut set is `M0772-X-MATHLIB-BODY`. The obligation-tree phase checks architecture
and conditional composition only. Proof acceptance, source/provenance closure, `AUDIT-Z`,
`THEOREM-Z`, hermetic replay, independent validation, and master acceptance remain open.
