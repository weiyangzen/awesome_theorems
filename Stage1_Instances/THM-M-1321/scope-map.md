# Scope map

## Candidate included claim

- A compact, connected Riemannian manifold `M` without boundary.
- Nonnegative Ricci curvature.
- The first positive (equivalently, first nonzero under the usual sign convention)
  Laplace-Beltrami eigenvalue `lambda1`.
- Riemannian diameter `d` and the sharp lower bound `lambda1 >= pi^2 / d^2`.

This is the classical reading of "Zhong-Yang estimate", not yet the canonical target. The exact
source theorem must decide dimension, regularity, sign and eigenvalue-index conventions, and how
zero diameter or the one-point case is excluded.

## Source ambiguity to resolve

The repository metadata says "convex domain". The statement phase must determine whether this is
an erroneous description of the manifold theorem or an intended Euclidean convex-domain Neumann
eigenvalue inequality. These are not interchangeable, and no broadened theorem may cover both.

## Explicit exclusions

- The Payne-Weinberger convex-domain inequality substituted without correcting source identity.
- Dirichlet eigenvalues, higher eigenvalues, negative Ricci lower bounds, or manifolds with boundary.
- A finite-dimensional matrix surrogate for the Laplace-Beltrami spectrum.
- A structure that assumes the eigenvalue bound as a field.

The later Lean statement must use concrete Riemannian distance, diameter, Ricci curvature, Laplacian,
and spectral interfaces, or document a precise missing-API blocker.
