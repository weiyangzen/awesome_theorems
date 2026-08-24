# Full study — one-variable Zariski cancellation

## N1-frozen-statement

For a field `k`, the target says that the one-variable polynomial algebra `k[X]` is cancellative. The hypotheses quantify a comparison algebra `B` with commutative-ring, `k`-algebra, and finite-type structures. The formal anchor is the frozen provider declaration. Its downstream use is semantic identity. The exceptional case is that the provider proof is sorry-backed, so its body is outside the trust boundary.

## N2-transparent-expansion

Transparent expansion retains every quantifier and structure: for each eligible `B`, `Nonempty (k[X][X] ≃ₐ[k] B[X])` implies `Nonempty (k[X] ≃ₐ[k] B)`. The inference is definitional transport, its output is the expanded proposition, and its formal anchor is `source_to_target` plus `target_to_source`. Downstream proof nodes consume this exact type. No local notation, definition, alias, coercion, or substituted import may change it.

## N3-stable-equivalence-input

The substantive input is a nonempty `k`-algebra equivalence between the two stabilized algebras. It is a caller-supplied hypothesis, not a theorem or oracle. Its output is an inhabitant available to the application node, its formal anchor is `cancellation_application`, and its downstream use is exactly once. The exceptional case is the empty `Nonempty`, in which the implication is not invoked; this is ordinary implication semantics, not a hidden assumption.

## N4-composition

The composition node specializes the universally quantified cancellation closure at the same `B` and its same typeclass instances, then applies it to the stable equivalence. Its output is `Nonempty (k[X] ≃ₐ[k] B)`, its formal anchor is `cancellation_application`, and its downstream use is the universal closure node. Universe parameters are explicit to prevent accidental transport between different algebra universes. The trust boundary is Lean kernel type checking at trust zero.

## N5-closure

The final node universally abstracts the comparison algebra and yields the exact expanded cancellation proposition. Bidirectional audit declarations reconstruct the same type, and the release node consumes this machine result. The formal anchors are `cancellation_composition` and `audit_composition`. The exceptional case remains the frozen sorry-backed source body, which is excluded from the observed target axioms; canonical Master recomputation is still required.
