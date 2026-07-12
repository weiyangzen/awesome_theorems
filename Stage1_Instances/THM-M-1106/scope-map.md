# Scope map

## Provisional included family

- A sequence of rectangular random data matrices whose row and column dimensions both diverge.
- A normalized sample covariance matrix, represented as either `X X*` or `X* X` after the exact
  dimension and scaling convention is fixed.
- A dimension ratio tending to a finite positive parameter.
- The empirical spectral distribution that assigns equal mass to the eigenvalues, including the
  source-specified treatment of forced zero eigenvalues.
- Convergence of that random probability measure to the Marchenko-Pastur distribution, in the
  topology and probabilistic mode required by the selected theorem.

This is a theorem family rather than a frozen proposition. Standard formulations vary between
real and complex entries, independent identically distributed entries and more general dependence,
almost-sure and in-probability convergence, finite-variance and stronger moment assumptions, and
reciprocal aspect-ratio conventions.

## Decisions required at statement freeze

The statement phase must freeze the scalar field; matrix orientation and dimensions; entry
independence, centering, variance, and moment/tail assumptions; covariance population (identity or
general); normalization; aspect-ratio convention and endpoint behavior; empirical-measure
normalization; convergence mode and test-function class; and the exact density, support, parameter,
and zero atom of the limiting measure.

Boundary cases must be explicit: ratio below, equal to, or above one; the corresponding rank defect
and zero atom; a ratio tending to zero or infinity; zero variance; noncentered or heavy-tailed
entries; real versus complex adjoint; repeated eigenvalues; and whether the theorem is stated along
one deterministic dimension sequence or uniformly over a family.

## Explicit exclusions

- A finite-dimensional eigenvalue computation or an expectation formula in place of convergence
  of empirical spectral measures.
- The Wigner semicircle law, Tracy-Widom edge fluctuations, universality, local laws, or the
  deformed/free multiplicative-convolution variants.
- Assuming convergence to the Marchenko-Pastur measure as structure data.
- Silently exchanging `p / n` with `n / p`, or `X X*` with `X* X`, without transporting the zero
  eigenvalue mass and empirical normalization.
- Treating plots, simulations, the repository label `已验证`, or a bibliographic citation as proof.

The later Lean target must expose the random-matrix hypotheses, spectral empirical measure,
limiting parameter, convergence predicate, and limiting measure rather than hide the conclusion in
an opaque assumption.
