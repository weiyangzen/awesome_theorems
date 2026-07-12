# Scope map

## Included theorem family

- A permutation chosen uniformly from the symmetric group on `N` letters.
- The length `L_N` of a longest strictly increasing subsequence in its one-line representation.
- Centering at `2 * sqrt N` and fluctuations on the `N^(1/6)` scale, subject to the exact
  normalization in the selected primary statement.
- Convergence of the distribution function of the normalized `L_N` to the Tracy-Widom
  distribution identified by the source.

## Decisions required at statement freeze

The statement phase must inspect and select the exact primary theorem, then freeze: the finite
permutation sample space and uniform measure; indexing convention; strict versus weak increasing
subsequence; the maximum and empty-size conventions; whether floors or integer thresholds appear;
the precise centering and scaling; the limiting distribution's analytic definition and
normalization; whether convergence is pointwise for every real argument or only at continuity
points; and the binder order between the real threshold and the limit in `N`. It must also decide
whether `N = 0` is excluded and how real powers and square roots are encoded.

These choices affect the exact proposition and cannot be inferred from the theorem name alone.

## Explicit exclusions

- The Robinson-Schensted correspondence by itself, or a finite identity for the distribution of
  longest increasing subsequences.
- An expectation, variance, tail bound, or law of large numbers without the fluctuation limit.
- The largest-eigenvalue Tracy-Widom theorem for a random-matrix ensemble as a substitute for the
  random-permutation conclusion.
- Longest common subsequences, random words, involutions, or nonuniform permutation models.
- Numerical sampling of permutations or numerical evaluation of a Painleve equation.
- A structure or hypothesis that assumes the desired convergence or limiting distribution.
- The repository label `已验证` as human-source or kernel evidence.

No canonical Lean expression is frozen at intake. A later statement must expose the finite uniform
probability model, longest-increasing-subsequence statistic, normalization, and distributional
limit rather than package the conclusion as input data.
