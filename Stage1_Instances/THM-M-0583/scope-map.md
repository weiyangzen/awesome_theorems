# Scope map

## Included claim

- Domain: a topological manifold of dimension exactly four, without boundary, closed (compact),
  and with the separation/countability conditions required by the selected manifold model.
- Hypothesis: the manifold is homotopy equivalent to the standard topological 4-sphere.
- Conclusion: a homeomorphism exists between the manifold and the standard 4-sphere.
- The later statement phase must decide whether connectedness and simple connectivity are explicit
  binders or consequences of the homotopy-equivalence hypothesis, without strengthening the claim.

This formulation is the homotopy-sphere form of the topological four-dimensional Poincare theorem.
An equivalent simply-connected homology-sphere formulation may only be admitted via checked
transports after its exact hypotheses are audited.

## Boundary cases to freeze

- `Manifold` versus a bare topological space carrying a manifold structure.
- Manifolds with boundary are excluded; compactness and Hausdorff/second-countability conventions
  must be explicit or inherited transparently from a pinned structure.
- Oriented versus unoriented formulations: orientation should not be added unless the source or a
  checked equivalence requires it.
- Homotopy equivalence is unpointed unless the source says otherwise.
- The standard sphere must be the topological `S^4`, not a combinatorial or smooth sphere encoding.

## Explicit exclusions

- The smooth four-dimensional Poincare conjecture, diffeomorphism to the smooth 4-sphere, and any
  claim about exotic smooth 4-spheres.
- The three-dimensional theorem, dimensions at least five, the h-cobordism theorem alone, or the
  classification of arbitrary simply connected topological 4-manifolds.
- A conclusion weakened to homotopy equivalence, since that is already a hypothesis.
- An abstract predicate or assumed homeomorphism that makes the result tautological.
- The metadata label `已验证` and legacy artifacts as proof or acceptance evidence.

The statement phase must freeze universes, ordered binders, manifold conventions, imports,
declaration type, environment fingerprint, transports, and hypothesis/boundary mutations.
