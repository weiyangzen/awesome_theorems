# Scope map

## Included subject boundary

- A local index theorem relating a small-time heat-kernel supertrace density to a characteristic
  form, for the geometric operator and closed smooth manifold selected from a primary source.
- The bundles, grading, elliptic or Dirac-type operator, heat kernel, diagonal restriction,
  supertrace, volume density, and characteristic forms used by that selected statement.
- The distinction between pointwise/form-level local convergence and the integrated global index
  formula, including all orientation, sign, and characteristic-class normalization conventions.
- Boundary decisions for odd versus even dimension, disconnected or zero-dimensional manifolds,
  manifolds with boundary, real versus complex bundles, and general elliptic versus Dirac-type
  operators.

## Required source decision

The metadata names only a theorem family. It could denote the local Gauss-Bonnet theorem for the de
Rham complex, a local Riemann-Roch/Dolbeault formula, a Dirac-operator local index theorem, or the
general local Atiyah-Singer density statement. These differ in hypotheses, density, characteristic
forms, convergence mode, and normalization. The statement phase must select one verbatim theorem
from a stable primary source and preserve every hypothesis and convention.

## Explicit exclusions

- Replacing the local density equality by the integrated global index theorem.
- Substituting Gauss-Bonnet, finite-dimensional rank-nullity, or a toy heat kernel without an
  explicit source establishing that it is the intended root.
- Assuming the desired density formula, index equality, or unnamed analytic facts as hypotheses.
- Treating nearby mathlib manifold/topology APIs or the legacy source-status label as proof.

The statement phase must freeze universes, manifold and bundle models, operator domains,
ellipticity/Dirac hypotheses, compactness and boundary assumptions, heat-kernel semantics,
characteristic forms, equality/convergence type, imports, declaration type, environment
fingerprint, checked transports, and hypothesis/boundary mutations.
