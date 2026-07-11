# Scope map

## Included claim

- A finite-dimensional compact connected Riemannian manifold without boundary.
- Nonnegative Ricci curvature.
- The first positive eigenvalue of the nonnegative Laplace-Beltrami operator on functions.
- A quantitative lower bound expressed using the Riemannian diameter, with the exact Li-Yau
  constant and Laplacian convention taken from the inspected primary theorem.

## Decisions reserved for the statement phase

The source inspection must fix dimension restrictions, smoothness and completeness assumptions,
connectedness as an assumption or consequence, the sign convention for the Laplacian, the precise
definition of the first nonzero eigenvalue, and whether diameter zero or zero-dimensional cases are
excluded. It must also determine whether the published estimate is stated directly as an
eigenvalue theorem or obtained as a corollary of a gradient estimate. Binder order, universes, and
the representation of the spectrum must follow those choices.

## Explicit exclusions

- The Li-Yau differential Harnack/heat-equation gradient estimate as a substitute for the Stage0
  eigenvalue claim.
- The later sharp Zhong-Yang diameter bound, which is separately tracked as `THM-M-1321`.
- Bounds involving negative Ricci lower bounds, boundary conditions, weighted manifolds, graphs,
  or discrete Laplacians unless they are required intermediate generality in the selected source.
- A structure or hypothesis that assumes the desired eigenvalue inequality.
- A finite-dimensional matrix eigenvalue inequality presented as the geometric theorem.

The later Lean target must expose concrete metric, Ricci curvature, Laplace-Beltrami spectrum, first
positive eigenvalue, and diameter interfaces, or record the exact missing mathlib API.
