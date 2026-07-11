# Scope map

## Included theorem family

- A finite discrete-time real-valued submartingale or martingale on a filtered probability space.
- The running maximum through a fixed terminal index.
- The weak `L1` estimate controlling the probability that the maximum crosses a positive level,
  and/or the strong `Lp` moment inequality for `p > 1`, according to the exact selected source.
- The source's precise use of the positive part, absolute value, or norm at the terminal time.

## Decisions required before statement freeze

The statement phase must select a stable primary theorem and fix the weak or strong variant,
submartingale versus martingale domain, scalar or normed-space codomain, finite index type, filtration
and adaptedness conventions, integrability class, `p` range, conjugate-exponent constant, and whether
the maximum is `max X_k`, `max |X_k|`, or a supremum. It must map null events, `p = 1`, zero threshold,
zero terminal index, and extended-real versus real-valued norms explicitly. Binder order and all
measurability hypotheses must be preserved.

## Explicit exclusions

- Doob's convergence, decomposition, optional sampling, or upcrossing theorem as a substitute.
- A deterministic finite-sequence maximum inequality with no filtration or conditional expectation.
- A weak tail inequality silently presented as the strong `Lp` result, or conversely.
- An estimate for nonnegative submartingales substituted for an absolute-value martingale statement
  without a checked reduction.
- An abstract structure that assumes the desired maximal estimate as a field.

The later formal statement must expose the stochastic-process, filtration, maximum, integrability,
and constant choices, or record a precise library API blocker.
