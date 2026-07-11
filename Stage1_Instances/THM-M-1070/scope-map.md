# Scope map

## Included mathematical object

- A stochastic process `X_t` indexed by nonnegative real time on one probability space, with a
  measurable state space that the statement phase must select (typically a real vector space or
  an additive topological group with sufficient measurable structure).
- `X_0 = 0` almost surely.
- Independent increments in the joint finite-family sense: increments over every finite family of
  pairwise disjoint, time-ordered intervals are independent. Pairwise independence alone is not a
  permitted weakening.
- Stationary increments: the law of `X_(s+t) - X_s` depends only on `t`, with all measurability and
  equality-in-distribution requirements explicit.
- Stochastic continuity: `X_s` converges to `X_t` in probability as `s` tends to `t`.
- Cadlag sample paths only according to the selected source convention: they may be included in
  the definition, supplied by a chosen modification, or proved as a regularization theorem.

## Statement-phase decisions

The exact source must settle the codomain, filtration (if any), completed/right-continuous
augmentation assumptions, whether equality is pointwise or almost sure, and the definition of
independence for random variables or generated sigma-algebras. It must also settle whether the
named deliverable is a definition package, existence of a cadlag modification, a characterization,
or another theorem about Lévy processes. Ordered binders, typeclass assumptions, universes, and the
boundary cases `t = 0`, repeated endpoints, empty/singleton interval families, and null exceptional
sets remain statement-gate work.

## Explicit exclusions

- A process merely assumed to have the desired fields followed by a restatement of those fields as
  the completed theorem.
- Pairwise independence substituted for joint independence of every finite increment family.
- Stationary one-time marginals substituted for stationary increment laws.
- A discrete-time random walk, Poisson process, Brownian motion, subordinator, or compound Poisson
  process substituted for the general Lévy-process target.
- Lévy-Itô decomposition or Lévy-Khinchin representation, which are separate repository targets.
- Dropping stochastic continuity or silently building cadlag regularity into the definition to
  avoid the source's regularization obligation.

The later formal target must expose a mathematically substantive and source-faithful deliverable;
an abstract structure populated entirely by hypotheses is useful infrastructure but not machine
closure of this target.
