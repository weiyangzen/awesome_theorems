# Scope map

## Literal scope and provisional claim family

The literal repository phrase "MCMC methods" denotes a methodology rather than a theorem. A legal
downstream correction must select one theorem about a named Markov-chain sampler. Its scope must
expose:

- a measurable state space and target probability measure;
- a concrete Markov transition kernel, including proposal and acceptance rules when applicable;
- initialization and every irreducibility, aperiodicity, recurrence, reversibility, integrability,
  or drift/minorization hypothesis used by the source;
- one exact conclusion, such as invariance, reversibility, convergence in total variation, an
  ergodic-average law, consistency, or a quantitative rate.

This list bounds a family; it is not a conjunction and is not yet a proposition. The statement
phase must either select a source theorem whose identity remains faithful to `THM-M-1100`, or record
that the target requires an integration-lane decision because the source entry is ill-posed.

## Decisions required at statement freeze

Freeze the source edition and pinpoint result; discrete versus continuous time; finite, countable,
or general measurable state space; normalized versus unnormalized target; proposal symmetry;
acceptance probability; kernel composition order; initial law; convergence topology or estimator;
quantifier order; and all degenerate cases. In particular, address zero target density, rejected
moves, reducible or periodic chains, null-support proposals, non-normalizable weights, and targets
without a stationary probability.

The 1953 algorithm is specialized to symmetric trial moves and canonical-ensemble weights. A more
general proposal correction belongs naturally to the distinct Metropolis-Hastings target unless a
checked specialization establishes exact identity without broadening this item.

## Explicit exclusions

- Treating an algorithm, implementation recipe, simulation, or empirical performance claim as a
  mathematical theorem.
- Substituting "every Markov kernel has an invariant probability" or "every MCMC chain converges";
  both are false without substantial hypotheses.
- Assuming the target law is invariant, detailed balance, ergodicity, or the desired convergence as
  a field of an abstract structure and then presenting the projection as the MCMC theorem.
- Replacing this item with the generic Metropolis-Hastings algorithm, Gibbs sampling, Hamiltonian
  Monte Carlo, or a finite-state stationary-distribution theorem.
- Giving proof credit to metadata `已验证`, a bibliographic citation, API availability, or a theorem
  name without an exact source-to-Lean statement match.

The checked `IntakeProbe.lean` only confirms that the pinned environment exposes Markov-kernel and
invariance vocabulary. It is not the canonical statement and proves no MCMC result.
