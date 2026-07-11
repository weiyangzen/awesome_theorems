# Scope map

## Preserved source scope

- Subject: a Riemannian metric evolving by Ricci flow.
- Object: an entropy functional introduced by Grigori Perelman in 2002.
- Repository wording: "the entropy functional for Ricci flow"; no formula or theorem is supplied.
- Plausible source family: the F-functional and its monotonicity, the W-functional and its
  monotonicity, and the associated lambda or mu quantities.

The alternatives are recorded as ambiguity, not interchangeable formulations.

## Decisions required before statement freeze

The statement phase must select a cited result and freeze: F versus W versus a derived invariant;
compactness, boundary, dimension, and smoothness assumptions; time interval and Ricci-flow sign
convention; the auxiliary function or probability density and its evolution/normalization; the
functional constants and scalar-curvature/Laplacian conventions; equality cases; and whether the
claim is a definition, first-variation identity, monotonicity formula, or rigidity theorem. It must
also freeze all ordered binders, endpoint behavior, and the exact Lean geometric/analytic APIs.

## Explicit exclusions

- Treating the definition of an entropy functional as its monotonicity theorem.
- Replacing Perelman's functional by Hamilton entropy, reduced volume, or a generic Lyapunov
  functional.
- Choosing F, W, lambda, or mu solely because one is easier to encode in Lean.
- Treating the metadata label `verified` as source or kernel evidence.
- Claiming a finite-dimensional analogy or abstract monotone real-valued function as the theorem.
