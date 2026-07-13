# Scope map

## Included subject boundary

- A source-selected Klein or Beltrami-Klein presentation whose points lie in the interior of a
  projective conic or quadric, commonly represented by an affine disk or higher-dimensional ball.
- The exact hyperbolic structure selected by the source: a cross-ratio distance, metric or
  Riemannian structure, incidence/geodesic structure, or an explicitly related package.
- The exact meaning of "projective model of hyperbolic geometry": satisfaction of a chosen axiom
  system, equivalence or isometry with a separately constructed hyperbolic space, or another
  source-defined relation.
- Every source-stated conclusion about chords, geodesics, projective transformations, curvature,
  completeness, topology, or boundary behavior, but only if it belongs to the selected theorem.

These bullets delimit the recognizable topic. They are not an accepted canonical statement.

## Decisions required at statement freeze

1. Select and independently inspect an immutable primary or authoritative source with exact
   definition, theorem, section, and page locators, proof boundary, corrections, and errata.
2. Decide the dimension and carrier: an affine open disk, a real ball, the interior of a conic or
   quadric in projective space, or another source-defined realization. Prove representation
   transports rather than treating them as definitional.
3. Freeze the field, ambient vector space, homogeneous-coordinate quotient, quadratic form and
   signature, affine chart, convex domain, and all nondegeneracy and orientation conventions.
4. Freeze the distance or line element and its normalization. Cross-ratio order, logarithm base,
   sign, absolute value, and factors such as `1/2` change the resulting formula and scale.
5. State what "model" proves: metric laws, hyperbolic incidence or parallel axioms, geodesic
   characterization, constant curvature and completeness, a transformation-group result, an
   isometry/equivalence, or a source-selected conjunction of these facts.
6. If straight chords are geodesics, define projective lines, affine chords, endpoints on the
   boundary, parametrization, maximality, uniqueness, and the relationship to the chosen metric.
7. If a symmetry statement is included, freeze the precise group, its action, the conic-preserving
   subgroup, effectiveness or quotient by scalars, and whether all isometries are characterized.
8. Decide whether and how equivalences with the hyperboloid, Poincare disk, or upper-half-plane
   models enter the root. Each credited direction needs a checked transport.
9. Resolve coincident points, the center, boundary and ideal points, tangent or degenerate chords,
   zero denominators, cross-ratio order, collinearity, low dimensions, and orientation reversal.
10. Freeze ordered binders, universes, structures, instances, coercions, all hypotheses, exact
    conclusion, foundation profile, and credited alternate encodings before proof search.

## Explicit exclusions

- Treating the title or the definition of a disk, projective space, distance, or structure alone as
  the requested theorem when no truth-valued property has been source-selected.
- Substituting only chord convexity, only a distance formula, only a geodesic description, only
  curvature/completeness, only an axiom-model result, or only an isometry when the selected root
  differs.
- Replacing this target with `THM-M-0218` (Poincare disk) or `THM-M-0219` (Poincare half-plane), or
  borrowing their artifacts without a checked theorem-specific bridge.
- Using the Euclidean metric inherited by an open disk as the Klein hyperbolic metric.
- Assuming the desired metric laws, model axioms, geodesic facts, curvature, completeness, group
  action, or isometry as fields and then merely projecting those fields.
- Confusing mathematical projective space with category-theoretic projective objects, the Klein
  four-group, a Klein-Gordon equation, or any other namesake.
- Crediting a theorem name, API elaboration, bounded no-match search, or `已验证` as statement
  identity, source fidelity, or proof evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, adjacent APIs provide `Complex.UnitDisc`, convex
metric balls, affine segments, projectivization of vector spaces, its general-linear action, and
`Matrix.ProjGenLinGroup`. They do not select a projective-ball carrier, define a Klein-model
distance, establish a hyperbolic model, or prove an inter-model transport. The probe and bounded
search are feasibility observations only, not the downstream immutable anchor audit.
