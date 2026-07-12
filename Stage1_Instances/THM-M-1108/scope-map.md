# Scope map

## Included theorem family

- A permutation chosen uniformly from the symmetric group on `N` letters.
- The length `L_N` of a longest strictly increasing subsequence in its one-line representation.
- Centering at `2 * sqrt N` and fluctuations on the `N^(1/6)` scale, subject to the exact
  normalization in the selected primary statement.
- Convergence of the distribution function of the normalized `L_N` to the Tracy-Widom
  distribution identified by the source.

## Decisions frozen by the statement phase

The source is Theorem 1.1 of arXiv:math/9810105v2. The finite sample space is
`Equiv.Perm (Fin N)` with uniform probability expressed as a cardinality ratio. Subsequences are
strictly increasing in both indices and values. The target includes `N = 0` as a harmless initial
term of the sequence; this cannot affect `atTop`. It uses exactly `2 * Real.sqrt N` and real power
`N^(1/6)`, with pointwise CDF convergence for every `t : Real`. The Tracy-Widom CDF is exposed by
the source's Airy/Painleve II asymptotics and integral formula rather than assumed as an opaque
arbitrary distribution.

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

The canonical Lean expression is now frozen in `Statement.lean` and exposes each of these
components. The exclusions above remain unchanged.
