# Source-statement crosswalk

## Candidate primary source

Peter Li and Shing-Tung Yau, "Estimates of eigenvalues of a compact Riemannian manifold," in
*Geometry of the Laplace Operator*, Proceedings of Symposia in Pure Mathematics 36, American
Mathematical Society (1980), pp. 205-239, is the primary-source candidate indicated by the title,
authors, date, and Stage0 phrase "lower bound for the first eigenvalue."

This bibliographic identification is discovery evidence, not `H0`. An exact theorem/corollary
number, page, wording, hypotheses, Laplacian normalization, constant, and errata check have not yet
been verified against a stable scan. No numerical formula is therefore frozen at intake.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Li-Yau estimate" | the 1980 spectral estimate selected by Stage0 context | named canonical theorem declaration | included; exact anchor open |
| "first eigenvalue" | first positive/nonzero scalar Laplacian eigenvalue | spectrum/eigenspace and least-positive-eigenvalue interface | included; normalization open |
| "lower bound" | quantitative inequality involving diameter | ordered-real inequality with source-exact constant | included; constant deliberately open |
| compact Riemannian manifold | geometric domain of the spectral theorem | compact smooth Riemannian manifold, likely boundaryless | included; dimensions/open edge cases |
| nonnegative Ricci curvature | geometric curvature hypothesis | pointwise Ricci lower-bound predicate | expected; source wording open |
| diameter | Riemannian metric diameter | metric diameter with finiteness proof | included |

## Identity and substitution guard

The same label commonly denotes Li and Yau's heat-equation gradient estimate. Stage0 explicitly
describes this target as a first-eigenvalue lower bound and dates it to 1980, so the spectral claim
is the intended identity. The statement phase must inspect the candidate paper and either locate the
exact spectral theorem or record an identity blocker; it must not replace the target with the heat
estimate or with Zhong-Yang's later sharp result.

No repository-local Lean candidate has been credited at intake. The anchor-audit phase must search
the pinned mathlib revision and credible external Lean 4 projects, recording exact declarations,
types, revisions, dependencies, axioms, and proof-body provenance.

Before `H0`, an independent reviewer must verify the source edition, exact theorem/page, all
assumptions, notation and normalization, derivation status, and known errata, then approve the
source-to-Lean mapping row by row.
