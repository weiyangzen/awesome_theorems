# Scope map

## Preserved theorem family

The intake preserves the hyperbolic-triangle cosine-law family named by the catalog. Its most
common side form relates side lengths `a`, `b`, and `c` to the interior angle `alpha` opposite `a`
by

```text
cosh(a) = cosh(b) cosh(c) - cos(alpha) sinh(b) sinh(c)
```

for curvature `-1`. Cyclic relabeling gives two further equations. This is a candidate scope
description supported by the inspected source lead, not the frozen canonical proposition.

## Decisions required at statement freeze

1. Select and independently approve an immutable primary or authoritative source and determine
   whether the repository intends the side law, the dual angle law, both, or all cyclic equations.
2. Fix the ambient hyperbolic plane and model: an abstract constant-curvature space, hyperboloid,
   Poincare disk, upper half-plane, or a checked equivalent encoding.
3. Fix the curvature or length normalization. For curvature `-k^2`, the formula uses `k * a`,
   `k * b`, and `k * c`; omitting this choice changes the claim.
4. Define a triangle, its geodesic sides, side lengths, interior angles, orientation conventions,
   and the correspondence between each side and its opposite angle.
5. Decide whether the root is one equation at a distinguished vertex, the conjunction of all
   three cyclic equations, or a universally quantified labeling-independent result.
6. Freeze ordered binders, typeclass assumptions, universes, coercions, conclusion, foundation
   profile, and every alternate encoding with a checked transport.
7. Decide whether antipodal-hyperbolic triangles or higher-dimensional triangles lying in a
   geodesic plane are included, and prove any transport to the selected two-dimensional theorem.
8. Specify whether degenerate, collinear, coincident-vertex, ideal, ultraideal, right, or zero-side
   cases are included, excluded, or handled by limiting statements.

## Boundary cases

Source review must explicitly resolve repeated vertices; zero side lengths; three collinear
vertices; angle `0` or `pi`; right triangles; equilateral and isosceles triangles; points tending
to the ideal boundary; ideal or ultraideal vertices; orientation reversal; cyclic relabeling; and
the Euclidean zero-curvature limit. The inspected Asmus theorem deliberately restricts its main
trigonometric analysis to non-degenerate triangles, so it does not settle all these policies.

## Excluded substitutions

- `Real.cosh_add`, `Real.cosh_sub`, or other scalar hyperbolic-function identities are not a
  geometric triangle theorem.
- `UpperHalfPlane.cosh_dist` relates two hyperbolic points to their Euclidean coordinates; it does
  not introduce three vertices, an angle, or the cosine law.
- The Euclidean law of cosines and the spherical law of cosines are different theorems.
- The hyperbolic law of sines, right-triangle identities, triangle inequality, angle-sum theorem,
  Gauss-Bonnet theorem, thin-triangle property, and distance formula are not substitutes.
- The dual law for angles is not silently interchangeable with the side law.
- A result assuming the desired cosine equation, or a structure storing it as a field, supplies no
  proof.
- A numerical example, floating-point check, theorem name, `#check`, or untrusted catalog label
  supplies no H or M credit.

## Neighbor boundaries

`THM-M-0214` separately owns the spherical cosine theorem. `THM-M-0213` owns the hyperbolic
parallel postulate, while `THM-M-0217`, `THM-M-0218`, and `THM-M-0219` own particular models of
hyperbolic geometry. `THM-M-0216` owns Gauss-Bonnet. Their definitions may later become explicit
dependencies or checked transports, but proximity grants no proof or scope credit.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the probe checks real `sinh`/`cosh` identities,
the upper-half-plane metric and `cosh_dist`, and the distinct Euclidean law of cosines. A bounded
search found no declaration for a hyperbolic triangle or its cosine law. This is scoped discovery
evidence, not an exhaustive anchor audit or a proof of global absence.
