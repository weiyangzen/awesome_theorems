# Scope map

## Included claim

- A finite dimension `n` satisfying `n >= 5`.
- A closed smooth `n`-manifold `M` (compact and without boundary, with the source's other
  conventions made explicit later).
- A homotopy equivalence `M ≃ S^n` as the recognition hypothesis.
- A homeomorphism `M ≅ S^n` as the conclusion.

## Boundary decisions for the statement phase

Primary-source inspection must determine connectedness, orientability, triangulation, and
differentiability conventions; whether dimension five is included without an auxiliary condition;
and whether the exact conclusion is homeomorphism, piecewise-linear equivalence, or a differently
phrased classification. Universes, binder order, the sphere model, manifold model, and the encoding
of dimension must then be frozen in the canonical Lean expression.

## Explicit exclusions

- The four-dimensional Poincare conjecture or the three-dimensional theorem.
- A diffeomorphism conclusion: exotic smooth spheres make that a materially stronger and generally
  false substitution.
- The h-cobordism theorem by itself, a simply-connected homology-sphere statement without checked
  equivalence to the chosen hypothesis, or a special case for a concrete sphere.
- An abstract structure that stores the desired homeomorphism as a field.

The later formal target must use concrete manifold, sphere, homotopy-equivalence, and homeomorphism
interfaces, or record exact missing APIs rather than weakening the theorem.
