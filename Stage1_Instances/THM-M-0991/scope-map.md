# Scope map

## Preserved source scope

The repository fixes only the named Berry-Esseen theorem and describes it as the rate of
convergence in the central limit theorem, attributed to Andrew Berry and Carl-Gustav Esseen around
1941. The intended theorem family is therefore a quantitative central limit theorem, not merely
weak convergence. The classical one-dimensional independent, identically distributed formulation
with finite third absolute centered moment and a uniform CDF error of order `1 / sqrt n` is the
candidate scope. It is not yet the accepted canonical claim.

## Statement decisions still required

The statement phase must freeze whether variables are identically distributed or only independent,
whether the mean is normalized to zero, whether variance is normalized to one, whether the third
moment is exact or bounded, and whether the constant is existential and universal or supplied as
data. It must also freeze positivity and nondegeneracy hypotheses, the CDF convention, normalization
of sums, the Gaussian variance parameter, the range `n > 0`, and the exact supremum-versus-pointwise
encoding. A primary edition, theorem/page, corrections, and every constant dependency must be
crosswalked before source fidelity can be accepted.

## Explicit exclusions

- The qualitative central limit theorem without a quantitative rate.
- Non-i.i.d., multivariate, local-limit, martingale, or nonuniform refinements unless the source
  audit identifies one as the catalog target.
- A proposition where the universal constant or the desired bound is supplied as an assumption.
- The metadata label `已验证`, or elaboration of a legacy statement boundary, as proof evidence.
- Any claim that mathlib's central limit theorem supplies the Berry-Esseen error estimate.
