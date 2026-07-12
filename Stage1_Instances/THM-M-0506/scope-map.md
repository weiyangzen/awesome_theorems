# Scope map

## Included topic boundary

- A source-selected theorem connecting a specified generalized summability method to ordinary
  convergence of a series or its partial sums.
- The exact coefficient sequence, scalar field, indexing convention, asymptotic side condition,
  and value asserted by that source.
- The definitions and analytic lemmas required for that exact implication.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different theorems commonly called
Tauberian:

1. **Tauber's original Abelian-converse form:** Abel summability of a power series together with a
   decay condition such as `n * a n -> 0` implies ordinary convergence to the Abel sum.
2. **Littlewood's strengthening:** a boundedness condition of order `a n = O(1/n)` replaces the
   original little-o condition.
3. **Hardy-Littlewood/Karamata forms:** positivity or monotonicity plus asymptotics of a generating
   function imply asymptotics of partial sums.
4. Wiener, Ikehara, or other Tauberian theorems for transforms, Dirichlet series, or convolution.

Even within item 1, a source must fix real versus complex coefficients, whether Abel summability is
expressed by `tsum (a n * r^n)` for every `0 <= r < 1`, the filter for `r -> 1`, the exact
asymptotic hypothesis, and whether partial sums use `range n` or `range (n + 1)`.

## Explicit exclusions

- Abel's limit theorem (ordinary convergence implies an Abel boundary limit) as a substitute for
  the converse Tauberian direction.
- Abel summation / summation by parts as a substitute for a Tauberian theorem.
- Littlewood, Karamata, Wiener, or Ikehara variants unless a pinned source identifies that variant.
- A finite-support special case, a positivity-only special case, or a tautology assuming the desired
  ordinary convergence.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one exact
member of the family.
