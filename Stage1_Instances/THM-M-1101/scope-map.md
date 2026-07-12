# Scope map

## Repository source boundary

The repository supplies the name "Metropolis-Hastings algorithm", attribution to
Metropolis/Hastings, the year 1970, and the gloss "MCMC's basic algorithm". It supplies no formula,
hypotheses, state space, or theorem conclusion. The label can refer to the transition construction,
its detailed-balance argument, target invariance, convergence under additional hypotheses, or the
resulting Monte Carlo estimator. Intake therefore freezes only the family, not a proposition.

## Provisional included family

- A target probability measure or unnormalized target density on a measurable state space.
- A proposal Markov kernel or proposal density, with a precisely specified reference measure.
- A source-specified acceptance probability, followed by rejection/staying at the current state.
- One exact source-selected correctness conclusion, commonly reversibility or invariance; any
  convergence or estimator conclusion must carry its additional hypotheses explicitly.

These components are a discovery map. They are not ordered binders and are not a Lean statement.

## Decisions required before statement freeze

The statement phase must inspect and select an exact primary-source result, then freeze the state
space, sigma algebra, target normalization, proposal representation, absolute-continuity and
support hypotheses, acceptance-ratio convention, treatment of zero numerator/denominator and
rejection mass, and whether the chain is time homogeneous. It must state precisely whether the
conclusion is detailed balance, stationarity, irreducibility, recurrence, convergence in total
variation, a law of large numbers, or an asymptotic variance comparison.

Binder order, universes, initial-state quantifiers, and boundary cases must be explicit. Important
cases include target-zero states, one-way proposals, atoms and mixed measures, an empty or singleton
state space, an identically rejecting proposal, reducible or periodic transitions, and targets
known only up to a multiplicative constant.

## Explicit exclusions

- Calling an algorithm description itself a theorem without a truth-valued conclusion.
- Proving only that an abstract kernel already assumed reversible is invariant and presenting that
  as construction or correctness of the Metropolis-Hastings transition.
- Substituting the symmetric-proposal Metropolis rule for the general Hastings rule.
- Claiming convergence or unbiased estimation from detailed balance alone.
- Assuming the desired target invariance, convergence, or estimator law as structure data.
- Treating simulation output, the metadata label `已验证`, or a generic mathlib theorem as proof of
  the unidentified source claim.

