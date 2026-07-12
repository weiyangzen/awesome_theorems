# Scope map

## Repository source boundary

Stage0 supplies only the name "Khasminskii ergodicity theorem," the gloss "ergodicity of diffusion
processes," the year 1960, and attribution to Rafail Khasminskii. It supplies no mathematical
formula, domain, hypotheses, or conclusion. Those metadata are insufficient for an exact theorem.

The planned root is the theorem family in Khasminskii's identified 1960 article concerning ergodic
properties of recurrent diffusion processes. This is a discovery scope, not a frozen statement.

## Decisions required before formalization

- Select a numbered theorem and exact wording from a stable copy of the primary article, and check
  whether the English translation preserves the original hypotheses.
- Fix the state space, diffusion construction, transition probabilities/semigroup, regularity and
  non-explosion assumptions, and the precise recurrence class.
- Fix whether an invariant measure is assumed or constructed, whether it is finite, and how it is
  normalized when a probability measure is needed.
- Fix the admissible observables or measurable sets, integrability/boundedness assumptions, the
  time parameter, and the time-average expression.
- Fix the conclusion: almost-sure, in-probability, distributional, mean, or transition-kernel
  convergence; also fix the quantification over initial states and any exceptional set.
- Record boundary cases such as null recurrence, infinite invariant measure, reducibility,
  explosion, disconnected state space, zero-time behavior, and non-integrable observables.

## Explicit exclusions

- A generic Birkhoff ergodic theorem detached from a diffusion process.
- Mere existence or invariance of a probability measure without the source's long-time conclusion.
- Ergodicity assumed as a hypothesis, or a structure containing the desired limit as data.
- A finite-state Markov-chain theorem, discrete-time chain theorem, or deterministic dynamical
  system theorem substituted for the recurrent-diffusion result.
- The parabolic Cauchy-problem stabilization results in the same article unless the selected source
  theorem explicitly makes them part of the root equivalence or conclusion.

## Expected formal surface, not yet credited

The eventual Lean target is expected to need measurable/topological state spaces, measures and
integration, a continuous-time Markov transition system or diffusion encoding, recurrence and
invariance predicates, time averages, and a precisely stated convergence relation. This inventory
does not assert that pinned mathlib supplies a diffusion-process abstraction or the terminal
theorem. That is for statement and anchor audit, not intake.
