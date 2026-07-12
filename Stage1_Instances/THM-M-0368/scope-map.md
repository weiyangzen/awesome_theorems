# Scope map

## Included theorem family

- The Hardy-Littlewood maximal operator formed from averages of a source-specified function over
  source-specified balls in a finite-dimensional Euclidean domain.
- A weak type `(1,1)` distribution estimate for positive thresholds.
- The exact measurability/integrability assumptions and dimension-dependent constant required by
  the selected source.
- The covering result and measure facts needed by the selected proof architecture.

## Decisions required at statement freeze

The source inventory does not resolve:

1. centered versus uncentered maximal operator;
2. open balls, closed balls, or cubes, and whether all radii or only positive radii are used;
3. scalar, real-valued, complex-valued, or extended-nonnegative input and whether the average uses
   `|f|`, `norm f`, or `enorm f`;
4. domain `Real`, `EuclideanSpace Real (Fin n)`, an arbitrary finite-dimensional normed space, or
   a doubling metric-measure space;
5. Lebesgue measure normalization and the exact dimension-dependent constant;
6. `lambda > 0` versus an extended-nonnegative threshold, strict versus non-strict superlevel set,
   and the treatment of infinite values;
7. `L1` as an equivalence class versus a measurable representative with a finite integral.

All ordered binders, universes, instances, hypotheses, the superlevel-set expression, and the
constant must be taken from an immutable source rather than reconstructed from the title.

## Explicit exclusions

- The strong `(p,p)` bound for `p > 1` as a substitute for weak `(1,1)`.
- The Hardy-Littlewood maximal *inequality* for sequences, ergodic maximal theorems, fractional
  maximal operators, or dyadic maximal operators.
- A differentiation theorem or a Besicovitch/Vitali covering theorem presented as the root claim.
- A definition followed by a tautological theorem, or an estimate with an assumed weak-type bound.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the available repository record is not an
exact mathematical statement.
