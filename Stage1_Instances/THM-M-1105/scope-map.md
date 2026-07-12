# Scope map

## Included theorem family

- A sequence of finite-dimensional real symmetric random matrices with independent entries on and
  above the diagonal, subject to the assumptions of the selected theorem.
- A normalization under which off-diagonal variance is of order `1/n` (or the equivalent scaling
  of an unnormalized matrix by `1/sqrt n`).
- The empirical spectral probability measure assigning mass `1/n` to each real eigenvalue,
  counted with algebraic multiplicity.
- Convergence of that random measure to a semicircle distribution. Under the common variance-one
  convention its density is `(1 / (2*pi)) * sqrt(4 - x^2)` on `[-2, 2]` and zero outside, but the
  selected source's scale is authoritative.

## Decisions required at statement freeze

The statement phase must select and inspect one exact theorem, then freeze: real or complex
ensemble; Hermitian/symmetric condition; independence and identical-distribution requirements;
diagonal law; centering; variance and scaling convention; finite-moment, boundedness, or Lindeberg
hypotheses; deterministic versus random matrix dimension; eigenvalue multiplicity convention;
weak convergence expressed through distribution functions, bounded continuous test functions, or
moments; convergence in expectation, probability, or almost surely; and exceptional null-set
quantifier order. It must also decide small dimensions, zero variance, atoms/heavy tails, and
whether the theorem concerns expected or sample empirical measures.

These choices are not cosmetic: they change binders, hypotheses, the limiting support, and the
strength of the conclusion.

## Explicit exclusions

- The Gaussian orthogonal ensemble alone as a substitute for a Wigner universality statement.
- The circular law, Marchenko-Pastur law, Tracy-Widom fluctuations, local semicircle law, or
  eigenvector universality.
- Convergence of only the largest eigenvalue, finitely many moments, or an expected density when
  the selected root asserts convergence of empirical measures.
- A finite numerical histogram or Monte Carlo experiment.
- A structure or hypothesis that assumes the desired spectral-measure convergence.
- The repository label `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. The statement must expose actual random
matrices, eigenvalues or spectral measures, measurability, and measure convergence rather than
package the conclusion as input data.
