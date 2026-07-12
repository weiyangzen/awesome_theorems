# Scope map

## Preserved source scope

- Subject: Hamiltonian Monte Carlo as a Markov-chain Monte Carlo method.
- State augmentation: a position variable with the target law and an auxiliary momentum variable.
- Proposal mechanism: Hamiltonian dynamics, usually approximated by a reversible,
  volume-preserving numerical integrator such as leapfrog.
- Correction mechanism: ordinarily a Metropolis accept/reject step and a momentum refresh policy.
- Historical locator supplied by the repository: Radford Neal, 2011.

This is an algorithmic subject boundary, not a theorem. The repository record supplies no domains,
ordered quantifiers, hypotheses, or conclusion.

## Decisions required before statement freeze

The statement phase must select one numbered or otherwise pinpointed source proposition. It must
freeze the position and momentum spaces, sigma algebras and reference measures; target density and
normalizing assumptions; kinetic energy and momentum law; smoothness, integrability, and ODE
existence assumptions; exact versus discretized flow; integrator step size and number of steps;
momentum negation/refresh convention; proposal and acceptance kernel; and the exact conclusion.

Possible conclusions are not interchangeable. Examples include preservation of the canonical
measure by exact Hamiltonian flow, detailed balance or invariance of a Metropolized HMC kernel, and
irreducibility, recurrence, or geometric convergence under much stronger assumptions. The source
must determine which one is the target. Binder order and universes must follow that choice.

Boundary cases also remain open: zero integration time, zero or invalid step size, an identity
proposal, acceptance probability zero or one, non-normalizable targets, nonsmooth or infinite
potentials, nonunique/explosive flows, degenerate mass matrices, constrained state spaces, and
partial versus full momentum refreshment.

## Explicit exclusions

- Treating pseudocode, a sampler implementation, or the name "HMC" as a proposition.
- Substituting invariance of exact Hamiltonian flow for invariance of the discretized Markov kernel.
- Omitting the Metropolis correction while claiming exact stationarity for an inexact integrator.
- Substituting generic Metropolis-Hastings correctness, symplectic volume preservation, or MCMC
  convergence without a checked specialization to the selected HMC kernel.
- Assuming the desired invariant law, detailed balance, or convergence result as structure data.
- Using numerical experiments, empirical acceptance rates, or the metadata label `已验证` as proof.

A later Lean target must expose the actual probability measure or density, augmented phase space,
flow or integrator, proposal, acceptance rule, and selected probabilistic conclusion. Missing
analysis or probability APIs must be recorded as blockers rather than hidden behind abstractions
that assume the result.
