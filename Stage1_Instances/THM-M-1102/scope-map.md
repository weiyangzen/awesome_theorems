# Scope map

## Preserved source scope

- Subject: a Markov chain Monte Carlo method commonly called Gibbs sampling.
- Update mechanism: sample one component or block from a conditional distribution while holding
  the remaining components fixed.
- Intended distributional context: a joint target distribution whose conditional distributions
  are used by the updates.
- Repository attribution: Stuart Geman and Donald Geman, 1984.

This is the complete mathematical scope justified by the repository record. It does not determine
one theorem or authorize a stronger convergence claim.

## Decisions required before statement freeze

The statement phase must select and inspect an exact primary theorem, then freeze:

- the product state space, sigma algebras, target probability measure, and existence/version of
  every regular conditional distribution;
- deterministic scan, random scan, systematic scan, or block-update scheduling, including update
  order and coordinate-selection probabilities;
- the transition kernel and whether the target conclusion is well-definedness, stationarity,
  detailed balance, invariance, irreducibility, recurrence, ergodicity, or convergence;
- positivity/support, accessibility, aperiodicity, Harris recurrence, and integrability conditions
  required by that exact conclusion;
- the convergence mode and strength, such as pointwise distribution, total variation, almost sure
  empirical averages, or a quantitative rate;
- finite, countable, standard-Borel, or more general measurable domains, plus zero-probability
  conditioning, empty-coordinate, singleton-state, and degenerate-support cases.

Binder order, universes, typeclass assumptions, foundation profile, and computation semantics must
follow those choices rather than be inferred from the topic name.

## Explicit exclusions

- Defining a Gibbs transition kernel and presenting its existence as a convergence theorem.
- Proving only target invariance and silently calling it ergodicity or convergence from every
  initial distribution.
- Replacing deterministic-scan Gibbs sampling by random-scan Gibbs sampling, since reversibility
  and transition structure differ.
- Assuming irreducibility, positivity, or the desired stationary law as structure fields and then
  treating a projection from that structure as the source theorem.
- Substituting the Gibbs distribution from statistical mechanics, a heat-bath dynamics result, the
  Metropolis-Hastings theorem, or simulated annealing.
- Treating the repository label `已验证` as a primary proof source or kernel receipt.

No legacy target-specific Lean module was found for this theorem ID. The later statement phase must
either provide concrete probability-kernel interfaces or record a precise pinned-mathlib API
blocker; adjacent Gibbs-weight code is not evidence for Gibbs sampling.
