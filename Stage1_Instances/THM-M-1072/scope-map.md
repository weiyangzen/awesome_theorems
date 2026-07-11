# Scope map

## Included theorem family

- A real-valued Levy process: it starts at zero, has stationary independent increments, and obeys
  the continuity condition selected from the exact source and formal process definition.
- The time dependence of each marginal characteristic function,
  `E[exp(i * u * X_t)] = exp(t * psi(u))`, subject to the selected Fourier-sign convention.
- A Levy-Khinchin representation of `psi` by drift, a nonnegative Gaussian coefficient, and a
  Levy jump measure satisfying the exact near-zero/tail integrability condition.
- Boundary instances including the zero process, deterministic drift, Brownian motion, compound
  Poisson processes, `t = 0`, `u = 0`, and any vanishing component of the triplet.

## Decisions required before statement freeze

The statement phase must pinpoint one exact theorem and fix the dimension, time domain, filtration
and adaptedness surface, stochastic-continuity/cadlag convention, characteristic-function sign,
Gaussian factor, truncation or compensation term, drift normalization, Levy-measure predicate, and
equality interpretation for integrals. It must decide from that theorem whether existence alone,
triplet uniqueness, the converse construction, or all three are root conclusions. Binder order,
measurability, probability, and integrability hypotheses must be explicit and mutation-tested.

## Explicit exclusions

- The representation theorem only for an arbitrary infinitely divisible probability law in place
  of the claimed process and all-time marginal statement.
- Levy continuity, Levy-Ito decomposition, or a compound-Poisson special case as a substitute.
- A finite-dimensional or Banach-space theorem silently replacing the real-valued target.
- A formula under one truncation convention combined with a drift from another convention.
- An abstract structure that assumes the desired characteristic exponent representation as data.

Any later use of the time-one law or a convolution semigroup must include a checked bridge back to
the process statement. The independently owned `THM-M-1023` and `THM-M-1024` dossiers provide no
statement or proof credit here.
