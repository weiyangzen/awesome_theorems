# THM-M-1479 scope map

## Preserved catalog scope

- Target identity: `THM-M-1479`, named `Monte Carlo方法`.
- Literal gloss: `基于随机采样的数值方法` (a numerical method based on random sampling).
- Catalog attribution and date: Stanislaw Ulam and John von Neumann, 1946.
- Recognizable boundary: numerical approximation or computation using random samples.

This is a method family, not one proposition. Intake preserves that ambiguity rather than silently
adopting the standard sample-mean convergence story.

## Proposition-changing decisions

An accountable source correction must select one immutable proposition and freeze:

1. The target quantity: an expectation, integral, event probability, count, solution functional,
   optimization objective, or another source-defined numerical object.
2. The input domain and measure: measurable space, probability or finite measure, normalization,
   integrand or observable, scalar/codomain, measurability, integrability, and moment assumptions.
3. The sampling model: iid, pairwise independent, stratified, importance-weighted, Markov-chain,
   sequential, dependent, pseudorandom, or another exact law, including initialization.
4. The estimator or algorithm: sample mean, weighted estimator, rejection or importance sampler,
   hit-or-miss estimator, transition kernel, branching process, or another recurrence/output.
5. The result: unbiasedness, consistency, almost-sure or probabilistic convergence, variance/MSE,
   CLT, concentration, confidence coverage, complexity, or another exact conclusion.
6. The quantitative conventions: sample count and indexing, normalization, finite versus
   asymptotic horizon, norm or metric, tolerance/confidence parameters, constants, and rates.
7. The computation boundary: ideal randomness versus PRNG, exact versus floating-point arithmetic,
   oracle calls, stopping rule, failure behavior, statistical certificate, and reproducibility.
8. Ordered binders, universe/typeclass context, implication directions, alternate encodings,
   degenerate cases, source corrections, and foundation/TCB/computation/freshness profiles.

Each choice changes the target's truth conditions and proof obligations. This list is a resolution
ledger, not a candidate statement.

## Candidate families not credited

- Unbiasedness of a source-selected sample-mean or importance-sampling estimator.
- Almost-sure, in-probability, or `L2` consistency of a source-selected estimator.
- A `1 / n` variance or mean-square-error identity under exact independence and moment premises.
- A CLT, Chebyshev, Hoeffding, or other finite/asymptotic error guarantee.
- An algorithm-specific Monte Carlo theorem for integration, probability estimation, transport,
  particle simulation, or optimization.

No candidate is selected, combined, or credited at intake.

## Neighbor ownership and exclusions

- `THM-M-0983` through `THM-M-0986` separately own law-of-large-numbers results; the pinned strong
  law and their repo-local wrappers do not identify this root.
- `THM-M-0987` and later entries separately own central-limit theorems.
- `THM-M-1100` through `THM-M-1103` own MCMC, Metropolis-Hastings, Gibbs sampling, and Hamiltonian
  Monte Carlo. No dependent-sampling algorithm may replace this generic numerical-analysis target.
- `THM-M-1480` owns quasi-Monte Carlo integration based on low-discrepancy sequences.
- `THM-P-0108` is a distinct physics target for statistical-mechanics random sampling, attributed
  to Metropolis/Ulam in 1949. Its wording and source family cannot be imported here.
- A deterministic quadrature theorem, numerical experiment, benchmark, sampled histogram,
  confidence interval computed from one run, or unchecked floating-point result is not a proof.
- A structure or hypothesis that stores the desired convergence or error conclusion cannot be
  projected as theorem evidence. The catalog's `已验证` label and a successful adjacent-API probe
  grant no H or M credit.

## Boundary cases

Source review must decide zero samples, the first sample/indexing convention, empty or zero-measure
spaces, non-probability measures, constant and almost-everywhere-equal observables, nonmeasurable or
nonintegrable inputs, infinite variance, zero error tolerance, confidence endpoints, zero-probability
events, signed or vector-valued outputs, dependent or identical samples, biased weights, stopping
times, nontermination, invalid random seeds, and exact versus finite-precision arithmetic. Intake
silently excludes none of them.

No canonical Lean target, checked transport, expression fingerprint, discovery protocol,
obligation registry, or proof state is frozen in this phase.
