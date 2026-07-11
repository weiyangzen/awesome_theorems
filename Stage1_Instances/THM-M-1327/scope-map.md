# Scope map

## Included theorem family

- A smooth Riemannian manifold, a base point `p`, and the distance function `r(x) = dist p x`.
- Evaluation only where `r` is smooth: outside `p` and the cut locus of `p` (or the precise
  substitute domain in the selected source).
- A sectional-curvature bound compared with a constant-curvature model.
- A quadratic-form/bilinear-form inequality for `Hess r`; equivalently, a bound on vectors
  orthogonal to the radial direction when the source states it that way.
- The source's model coefficient, normally expressed using the logarithmic derivative of the
  model Jacobi function, including its radius restrictions and limiting cases.

## Decisions reserved for statement phase

An inspected theorem must fix: curvature upper versus lower bound; complete versus local manifold;
dimension and connectedness assumptions; the geodesic/minimizing domain; sign convention for the
curvature tensor and Hessian; whether comparison is on all tangent vectors via the transverse
metric or only radial-orthogonal vectors; strict/non-strict inequalities; model curvature and
conjugate-radius restrictions; and boundary/zero-curvature cases. Binder order, universes, and all
Lean encodings remain open until those choices are frozen.

## Explicit exclusions

- Laplacian comparison (the trace consequence) as a substitute for Hessian comparison.
- Bishop-Gromov volume comparison, Rauch comparison alone, or a Euclidean-only Hessian identity.
- Swapping a sectional-curvature upper bound for a lower bound without reversing/rederiving the
  comparison.
- A global assertion across the cut locus where the classical distance function is not smooth.
- A structure or hypothesis that contains the desired Hessian inequality as assumed data.

The repository has no legacy Lean artifact for this target. A later exact statement must use
concrete Riemannian distance, Hessian, curvature, cut-locus/smooth-domain, and model-function APIs,
or record the exact missing interface.
