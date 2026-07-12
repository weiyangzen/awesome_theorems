# Scope map

## Provisional included family

- A discrete-time, time-homogeneous Markov chain on a general measurable state space, represented
  by a transition kernel `P`.
- A measurable Lyapunov function `V`, with codomain, lower bound, and integrability fixed by the
  selected source theorem.
- A source-exact negative-drift hypothesis toward a measurable small or petite set `C`. Candidate
  shapes include additive drift and geometric drift, but only one inspected source statement may
  become canonical.
- Every irreducibility, accessibility, aperiodicity, minorization, and regularity assumption used
  by that source result.
- Exactly the selected theorem's stability conclusion, such as positive Harris recurrence,
  existence of an invariant probability, an integrability estimate, or a specified convergence
  rate.

This is a theorem family, not yet a proposition. A drift inequality can be a hypothesis, a
definition, or one side of a characterization; the repository wording does not select among these.

## Decisions required at statement freeze

The statement phase must select an edition and numbered theorem, then freeze the state-space and
kernel model; discrete versus continuous time; the definition and codomain of `V`; the exact drift
operator (`PV - V`, a generator, or another form); the set predicate on `C`; constants and strictness
conditions; irreducibility and aperiodicity assumptions; and the exact conclusion. It must preserve
the source binder order and distinguish pointwise inequalities from almost-everywhere statements.

Boundary cases must be explicit: empty state space or drift set, unreachable `C`, reducible or
periodic chains, zero drift parameter, geometric factor equal to one, infinite values of `V`,
nonintegrable drift, and invariant measures that are sigma-finite rather than probabilities. If the
source uses a sampled or skeleton chain, its relationship to the original chain must be part of the
target.

## Explicit exclusions

- A definition of a drift condition with no stability consequence.
- Replacing a general-state-space result by a finite-state stationary-distribution theorem.
- Combining an additive-drift recurrence theorem with a geometric-drift convergence conclusion.
- Replacing a petite set by a small set, or conversely, without a checked implication under the
  selected hypotheses.
- Assuming recurrence, an invariant probability, or the desired convergence result as structure
  data.
- Treating a simulated negative drift, an informal citation, or the metadata label `已验证` as
  theorem evidence.

The later Lean target must expose the kernel expectation/iterate, measurability, drift inequality,
set condition, and stability conclusion rather than hide the desired result in an abstract package.
