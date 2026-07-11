# THM-M-1324 rev-5.6 intake

This is a `planned` dossier for Cheng's eigenvalue comparison theorem. The Stage0 label
`已验证` is untrusted metadata and supplies no proof credit.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Root comparison | first Dirichlet eigenvalue of a geodesic ball versus the equal-radius constant-curvature model ball | Exact theorem number and all radius qualifications require primary-source inspection |
| Geometry | complete finite-dimensional Riemannian manifold; Ricci lower bound `Ric >= (n-1)K` | Smoothness, connectedness, dimension edge cases, and curvature normalization remain to be frozen |
| Spectral object | bottom/first eigenvalue for the Dirichlet Laplacian | Laplacian sign and variational/eigenfunction encoding are not yet selected |
| Analytic route | radial model eigenfunction, distance/Laplacian comparison, Rayleigh quotient | Architecture only; no obligation or proof-body credit |
| Boundary cases | positive admissible radius; model cut/conjugate-radius restrictions | `r = 0` and non-admissible radii are excluded |
| Formal foundations | Lean 4, mathlib geometry, measure/integration, Sobolev and spectral APIs | No declaration or sufficient API is asserted to exist |

The closely related comparison with a sectional-curvature upper bound and the opposite eigenvalue
inequality is not silently merged into this root. The statement phase must resolve that possible
variant against the primary paper before constructing the Lean expression.

## Intake verdict

Lifecycle is `planned`; root vector is `[H2, M4, R3]`. The first failed gate is exact-statement
identification: the bibliographic paper is identified, but its theorem/page assumptions and errata
have not been inspected from an immutable source. Consequently no Lean target, proof, or completion
is claimed.
