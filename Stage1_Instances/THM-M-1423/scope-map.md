# Scope map

## Preserved source scope

The repository fixes only the Chinese label `耦合方法`, the gloss `随机系统的同步`
("synchronization of random systems"), the attribution `众多数学家` ("many mathematicians"),
the period "twentieth century," and an untrusted `已验证` status. It supplies no primary source,
theorem locator, definition, premise, or conclusion. The intake therefore preserves only a broad
random-dynamics coupling/synchronization topic boundary.

## Proposition-changing decisions

An approved statement correction must obtain an exact source and freeze all of the following:

- the probability/noise space, filtration or metric dynamical base, state space, measurable and
  metric/topological structures, and whether time is discrete or continuous and one- or two-sided;
- the random object: Markov kernel/process, stochastic differential equation, random map, flow,
  cocycle, or other source-specified system, including initial states and regularity assumptions;
- whether coupling means a joint probability measure with specified marginals, a joint process,
  common noise, a coupling kernel, or a proof-only construction, plus adaptedness, Markovian,
  co-adapted, maximal, reflection, or independence requirements;
- the synchronization predicate: exact equality, finite coupling time, metric contraction,
  convergence to one another, convergence to a common random point, or a singleton random
  attractor;
- the mode and strength of convergence: pathwise, almost surely, in probability, in expectation,
  or in distribution; pointwise versus uniform initial-state scope; rate and constants; and the
  placement of null sets relative to all other quantifiers;
- the sufficient hypotheses, such as contraction, order preservation, mixing, recurrence,
  dissipativity, Lyapunov-sign, minorization, irreducibility, compactness, or integrability; and
- one truth-valued conclusion, every ordered binder and premise, and all exceptional and boundary
  cases.

These choices yield inequivalent propositions. They are a resolution checklist, not a canonical
claim.

## Candidate families not credited

- Existence of some joint law with two prescribed marginals.
- Successful or coalescent coupling of two source-specified Markov processes.
- A coupling inequality that bounds total variation or another distance by a coupling event.
- Common-noise pathwise contraction or asymptotic pairwise synchronization.
- Weak synchronization expressed by convergence in probability to a random point.
- Strong or almost-sure synchronization of all initial conditions.
- A singleton random-attractor result under order, mixing, Lyapunov, or dissipativity hypotheses.

No family in this list is selected or credited at intake.

## Explicit exclusions

The intake must not silently replace this target with the separately cataloged random dynamical
systems topic (`THM-M-1424`), random attractors (`THM-M-1425`), or multivalued random dynamical
systems (`THM-M-1426`). A theorem about Markov-chain mixing, ergodicity, invariant measures,
Wasserstein contraction, total variation, Lyapunov exponents, stable manifolds, or stochastic-flow
coalescence is related only after a source selects it.

Skorokhod representation (`THM-M-1010`), Komlos-Major-Tusnady strong approximation
(`THM-M-1065`), and McCann optimal-transport existence (`THM-M-1186`) already own other important
uses of coupled variables or measures. Their common-space, strong-approximation, or transport-plan
conclusions cannot be borrowed as this target's synchronization statement.

Likewise excluded are mathlib's generic composition of Markov kernels, an independent product
measure presented as if it synchronized trajectories, equality in distribution presented as
pathwise equality, a deterministic coupled-oscillator theorem, a one-state or constant-map toy
system, a numerical simulation, and a structure that assumes the desired coupling or
synchronization conclusion as a field. None can identify or close the catalog topic.

## Degenerate and boundary scope

An exact source must decide empty or singleton state spaces, identical versus distinct initial
states, zero or infinite coupling time, failure to meet or converge, absorbing and deterministic
systems, degenerate or absent noise, nonunique solutions, nonmeasurable exceptional sets, finite
versus infinite distance, pseudometric zero without equality, and whether one null set works for
all initial conditions. It must also distinguish asymptotic distance zero from eventual equality
and equality of laws from equality of sample paths.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides adjacent measures and their
marginals, probability kernels and composition, Markov-kernel instances, identical-distribution,
metric, and filter-convergence APIs. A bounded topic-name search found no random-dynamics
coupling/synchronization declaration in pinned mathlib; unrelated uses of "coupling" occur in
Gromov-Hausdorff geometry. These facts show possible substrate only. They are not an anchor audit,
statement elaboration, or machine-proof evidence.
