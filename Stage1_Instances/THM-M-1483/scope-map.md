# THM-M-1483 scope map

## Preserved repository scope

The literal repository boundary is the label `粒子群优化`, the gloss `基于群体智能的优化`, and
the attribution to James Kennedy and Russell Eberhart in 1995. This identifies the particle-swarm
optimization algorithm family. It does not select one mathematical proposition.

A representative PSO model evolves a finite swarm of positions and velocities using personal-best
and neighborhood- or global-best positions, often with random multipliers. That description is
only a candidate family envelope. The original 1995 paradigms and later inertia-weight,
constriction-factor, topology, boundary-handling, and asynchronous variants have different state
transitions and mathematical behavior. Intake freezes none of them as the root.

## Decisions required at statement freeze

1. Select an immutable source proposition and decide whether the root concerns an algorithm
   definition, well-definedness, an invariant, equilibrium or stagnation, stability, convergence,
   a rate, global-optimum discovery, or another exact result.
2. Fix the PSO variant and every update equation, including update order, inertia or constriction,
   cognitive and social coefficients, personal-best rule, neighborhood topology, tie breaking,
   synchrony, and initialization.
3. Fix the particle index set, dimension, position and velocity spaces, admissible search region,
   boundary handling, objective codomain and regularity, and the existence or uniqueness assumptions
   for optima.
4. Fix the randomness model: deterministic parameters or random variables, probability space,
   independence and distribution assumptions, resampling policy, filtration, measurability, and
   quantifier order.
5. Define the observable and conclusion exactly: state boundedness, coefficient stability,
   convergence of particles or best values, almost-sure/in-probability/mean-square mode, rate,
   hitting probability, finite-time guarantee, or asymptotic global optimality.
6. Fix exact versus floating-point arithmetic, overflow and rounding behavior, stopping rules,
   iteration horizon, resource/cost model, and whether empirical benchmark performance is excluded.
7. Fix domains, universes, typeclasses, ordered binders, all hypotheses, exact conclusion,
   foundation/TCB/computation profiles, minimal imports, checked transports, and mutations.

## Boundary and degenerate cases

The statement phase must decide empty and singleton swarms; zero-dimensional or empty search
spaces; zero iterations; zero, negative, or exceptional coefficients; zero velocities; identical
particles; constant objectives; absent, multiple, or nonunique global minimizers; ties in personal
or neighborhood bests; disconnected or changing topologies; particles leaving a bounded domain;
degenerate random laws; dependent randomness; objectives with infinities or undefined values;
stagnation away from an optimum; and exact versus finite-precision execution.

No case is excluded at intake. Storing convergence, boundedness, an optimum witness, or discovery
of that witness as an input field would be circular if the selected root is meant to establish it.

## Candidate statements not credited

- A definition or executable specification of one PSO update rule.
- Well-definedness or preservation of a selected bounded search region.
- Stability or convergence of a deterministic linearized one-particle dynamical system under a
  selected coefficient inequality.
- Mean, mean-square, in-probability, or almost-sure convergence of a selected stochastic PSO model.
- Monotonicity of stored personal-best or global-best objective values.
- Eventual discovery of a global optimum on a finite domain under an explicit positive-exploration
  assumption.
- A convergence-rate, hitting-time, or finite-iteration approximation guarantee.

These candidates require different data and conclusions. A benchmark-success claim is empirical,
not a theorem transport. Intake admits none without an accountable source decision and independent
review.

## Neighbor and substitution exclusions

- `THM-M-1481` separately owns simulated annealing and `THM-M-1482` genetic algorithms; neither
  transfers proof or source status to particle swarm optimization.
- `THM-M-1479` and `THM-M-1480` separately own Monte Carlo and quasi-Monte Carlo methods; their
  probability or discrepancy results do not identify a PSO claim.
- `THM-M-1490` and `THM-M-1491` separately own optimization theory and convex optimization. Generic
  minimizer-existence or convex-optimality results are substrate, not a PSO theorem.
- A finite benchmark, favorable plot, numerical trace, implementation test, or observed best value
  cannot establish a universal convergence or optimality claim.
- A structure or hypothesis that stores the desired optimum, convergence, invariant, or update
  correctness supplies no proof.
- The catalog's `已验证` label and the discovery-only Lean probe supply no H or M credit.

## Formal and execution boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Finset.exists_min_image` supplies a minimum for a nonempty finite image,
`isFixedPt_of_tendsto_iterate` turns convergence of an iteration into a fixed point, and
`ContractingWith.tendsto_iterate_fixedPoint` supplies convergence for a contraction. None defines
particles, velocities, personal bests, neighborhood topology, a PSO update, or a PSO conclusion.

A bounded exact-topic search found no source-selected particle-swarm declaration in pinned mathlib
or repo-local Lean. This is intake discovery, not an exhaustive anchor audit or global absence
proof. Later phases own exact statement selection, candidate provenance, obligation freezing,
typed graphs, proof bodies, composition, trust, readable reconstruction, and release evidence.
