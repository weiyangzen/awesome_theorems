# Statement freeze

Item: `S56-M-0772-STATEMENT`

`Statement.lean` freezes the repository claim as follows: for every type `P : Type u` with a
`PartialOrder P` instance, there is a subset `c : Set P` satisfying
`IsMaxChain (fun x y => x <= y) c`. By mathlib's definition this means that `c` is a chain and every
chain containing `c` equals `c`. Thus maximality is under subset inclusion, not cardinality, and is
not maximal-element status in `P`.

The canonical declaration is
`Stage1Instances.THM_M_0772.HausdorffMaximalPrinciple`. Its sole direct import is
`Mathlib.Order.Preorder.Chain`, the minimal module declaring `IsChain` and `IsMaxChain`; the
construction module containing `maxChain_spec` is deliberately not imported at this phase.

The checked theorem `hausdorffMaximalPrinciple_iff_expanded` is reflexive after expanding
`IsMaxChain`, so it verifies the prose reading without invoking a maximal-chain existence proof.
The universe and binders are ordered as `P : Type u`, `[PartialOrder P]`, then the existential
`c : Set P`. There are no nonemptiness, finiteness, completeness, or choice hypotheses in the
formal target. `EmptyBoundary` and `SingletonBoundary` confirm that the corresponding specialized
propositions elaborate and remain in scope; they are not proofs of those propositions.

Four separately elaborated mutations remove the partial-order hypothesis, specialize the carrier
to `Nat`, change the universal carrier binder to an existential binder, or exclude the empty type.
The scoped checker compares their explicit elaborated expressions and rejects any mutation that
collapses to the canonical expression.

This artifact freezes and elaborates a statement only. The primary-source pinpoint review, audit of
`maxChain_spec`, proof-body and axiom provenance, obligation tree, theorem proof, hermetic replay,
and independent acceptance remain downstream tasks. No theorem completion is claimed.
