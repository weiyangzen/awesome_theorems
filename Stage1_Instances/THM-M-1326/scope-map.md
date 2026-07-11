# Scope map

## Included theorem family

- A complete finite-dimensional Riemannian manifold, a base point, and its distance function `r`.
- A pointwise lower bound on Ricci curvature, with dimension and curvature normalization explicit.
- An upper bound for `Delta r` by the radial Laplacian in the constant-curvature model space.
- A classical pointwise statement off the base point and cut locus, plus precisely the weak,
  distributional, viscosity, or barrier extension stated by the selected source.
- The zero-curvature specialization `Delta r <= (n - 1) / r` as a corollary only if transported from
  the canonical normalized statement.

## Decisions reserved for statement freeze

The inspected source must determine the sign convention for `Delta`, whether the curvature
parameter is `k`, `K`, or its square root, the model function and its domain before a conjugate
radius, connectedness and boundary assumptions, regularity, and the exact treatment of dimension
one, the base point, the cut locus, and positive-curvature radius restrictions. Binder order,
universes, tangent-space trace, and the Lean encoding of Ricci lower bounds remain open.

## Exclusions

- Hessian comparison, Bishop-Gromov volume comparison, Cheng eigenvalue comparison, or a heat-kernel
  estimate substituted for the Laplacian statement.
- A theorem only on Euclidean space or only along one geodesic.
- An assumption that directly packages the desired Laplacian inequality.
- Ignoring the cut locus, changing the Laplacian sign, or replacing Ricci by sectional curvature
  merely to match an available API.

