# THM-M-1481 scope map

## Catalog scope preserved

- Target identity: `THM-M-1481`, named `模拟退火` (simulated annealing).
- Catalog attribution and year: Scott Kirkpatrick, 1983.
- Literal gloss: `全局优化的随机方法` (a randomized method for global optimization).
- Subject boundary: temperature-controlled stochastic search motivated by physical annealing.

This is all the mathematical scope fixed by the repository. It does not determine a proposition.

## Decisions required before statement freeze

An accountable target correction must select one immutable source proposition and freeze:

1. The state space: finite configurations, a finite graph, countable states, or a measurable
   continuous space, including nonemptiness, topology, sigma algebra, and finiteness assumptions.
2. The cost or energy codomain, order, boundedness, measurability or continuity, and the exact set
   of global minimizers.
3. The move mechanism: neighbor graph or proposal kernel, connectivity, symmetry or positivity,
   self-loops, time homogeneity, and irreducibility assumptions.
4. The acceptance law: Metropolis or another rule, treatment of equal/downhill/uphill moves, inverse
   temperature convention, normalization, and zero-temperature behavior.
5. The deterministic or adaptive cooling schedule, indexing origin, positivity, monotonicity,
   logarithmic constants, and any energy-barrier or depth definition.
6. The stochastic process construction, initial state or distribution, randomness space, ordered
   binders, conditioning, and all Markov-kernel composition conventions.
7. The conclusion: convergence in probability to the minimizer set, concentration of marginals,
   almost-sure eventual behavior, stationary-law limit, finite-time success probability, expected
   hitting time, or only an algorithm-definition/correctness result.
8. Exact versus floating-point exponentials, underflow and random-number assumptions, stopping
   rules, computability, complexity, boundary cases, and every checked alternate encoding.

These choices change truth conditions and proof obligations. They are a resolution checklist, not
a canonical claim.

## Candidate theorem families not credited

- The 1983 Kirkpatrick-Gelatt-Vecchi framework and its concrete combinatorial applications.
- A finite-state inhomogeneous Markov-chain theorem that a source-specified cooling condition makes
  the state converge in probability to the global-minimum set.
- Hajek's necessary and sufficient cooling-schedule condition and its logarithmic-schedule
  corollary using the depth of the deepest nonglobal local minimum.
- Fixed-temperature Metropolis invariance or reversibility for a Gibbs distribution.
- Correctness or finite-time behavior of a particular implemented annealing heuristic.

None is selected, stated, or credited at intake. A definition of a transition kernel or proof of a
fixed-temperature invariant measure alone would not prove global optimization under cooling.

## Boundary and degenerate cases

The statement phase must resolve an empty or singleton state space, constant cost, every state
globally optimal, no global minimizer, disconnected proposal graph, isolated states, zero proposal
probabilities, self-loops, equal-energy moves, zero or negative temperature, infinite temperature,
schedule indexing at `0` versus `1`, logarithms at their boundary, a cooling rate above, at, or
below the critical depth, zero-depth landscapes, repeated minima, and arbitrary initial states.

It must also distinguish convergence of one-time marginals from almost-sure path convergence.
Inhomogeneous annealing need not have one stationary distribution, while a fixed-temperature Gibbs
invariance result does not by itself establish cooling-schedule convergence.

## Neighbor ownership and explicit exclusions

- `THM-M-1100` owns the general Markov chain Monte Carlo topic, `THM-M-1101` the
  Metropolis-Hastings algorithm, and `THM-M-1102` Gibbs sampling. Their invariant-kernel or
  convergence results may be dependencies but cannot replace this cooling/global-search root.
- `THM-M-1479` Monte Carlo methods and `THM-M-1480` quasi-Monte Carlo methods own sampling and
  integration families, not simulated-annealing convergence.
- `THM-M-1482` genetic algorithms and `THM-M-1483` particle-swarm optimization are alternative
  heuristic families and share no statement or proof credit.
- A finite-state minimum-existence lemma, Markov-kernel definition, invariance, reversibility,
  irreducibility, or generic convergence lemma alone is substrate, not simulated annealing.
- A theorem that assumes the desired convergence or optimizer identification as a field or
  hypothesis does not establish it.
- A finite experiment, successful benchmark, sampled trajectory, temperature plot, or unchecked
  random computation cannot substitute for a source-selected theorem.
- The catalog label `已验证`, a name match, or a successful `#check` supplies no H or M credit.

## Formal boundary

No canonical Lean expression is frozen. At the pinned mathlib revision, generic probability kernels
and the predicates `Kernel.Invariant`, `Kernel.IsReversible`, and `Kernel.IsIrreducible` exist,
as does `Finset.exists_min_image` for a finite minimum. A bounded exact-topic search found no
simulated-annealing, cooling-schedule, or Metropolis declaration matching the catalog. These are
intake discovery facts only, not a complete anchor audit or a global absence claim.
