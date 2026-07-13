# THM-M-1482 scope map

## Preserved repository scope

The literal repository boundary is the label `遗传算法`, glossed as `基于进化的优化算法` and
attributed to John Holland in 1975. This identifies the genetic-algorithm family: population-based
search using inherited variation and selection. It does not select one mathematical proposition or
one executable algorithm.

Candidate results that require separate source decisions include:

- a source-specific schema theorem about the expected representation of schemata after selection,
  crossover, and mutation;
- well-definedness or population-size preservation for one generation operator;
- invariance, irreducibility, hitting, or convergence properties of a finite-population Markov
  process;
- convergence of best-so-far fitness under explicit elitism and positive-mutation assumptions;
- correctness and termination of an executable implementation; and
- exact or asymptotic runtime, sample-complexity, or approximation guarantees.

None is the canonical target at intake.

## Decisions required before statement freeze

1. Admit and independently review an immutable primary source and select one exact theorem or
   algorithm-correctness proposition, including its incorporated definitions and proof boundary.
2. Fix the genotype/phenotype spaces, encodings, population carrier (sequence, multiset,
   distribution, or another model), population size, and every finiteness or measurability premise.
3. Fix the objective or fitness codomain, ordering, ties, scaling, constraint handling, and whether
   fitness is deterministic, noisy, time-dependent, or population-dependent.
4. Fix selection: proportional, rank, tournament, truncation, or another operator; with- or
   without-replacement semantics; normalization; and zero-total-fitness behavior.
5. Fix reproduction: arity, pairing, crossover points and distribution, recombination direction,
   mutation kernel and rate, independence assumptions, and validity preservation.
6. Fix replacement and elitism, generation indexing, randomness carrier, initial population law,
   stopping rule, and any best-so-far archive.
7. Fix the exact conclusion: an expectation identity or bound, schema survival, invariant law,
   reachability, almost-sure or in-probability convergence, optimizer discovery, implementation
   refinement, termination, or cost result.
8. Freeze ordered binders, hypotheses, universes, alternate encodings and transport directions,
   foundation/TCB/computation profiles, and every boundary case before elaboration.

## Degenerate and boundary cases to resolve

- empty and singleton genotype spaces; empty, singleton, and zero-size populations;
- zero, constant, negative, non-finite, or all-equal fitness values and undefined normalization;
- ties and nonunique optima, infeasible individuals, and invalid encodings;
- zero or unit crossover and mutation probabilities, no-op variation, and mutation without full
  support;
- odd population sizes, self-mating, duplicate parents, crossover of unequal encodings, and invalid
  offspring;
- generational versus steady-state replacement, complete generational loss, and presence or
  absence of elitism;
- finite versus infinite search spaces and time horizons; nontermination and stopping at generation
  zero; and
- exact probability versus pseudo-random or floating-point implementation semantics.

No case is excluded until a proposition is selected.

## Explicit non-substitutions

- The schema theorem, building-block heuristic, convergence to a global optimum, and no-free-lunch
  results are distinct statements and cannot be selected from the topic name alone.
- A toy bit-string search, oneMax objective, one individual, mutation-only process, or deterministic
  hill climber cannot replace an unidentified general target.
- An evolution strategy, genetic programming system, differential-evolution method, particle-swarm
  optimizer, simulated-annealing method, or biological-population theorem is a different target.
- A structure field or hypothesis storing desired correctness, convergence, or optimality is not a
  proof of that result.
- Generic `Multiset`, `Finset`, `PMF`, Markov-kernel, optimization, or expectation infrastructure is
  not a genetic-algorithm theorem.
- A simulation, benchmark, random-seed run, fitness curve, empirical success rate, or
  floating-point residual is not theorem evidence.
- The untrusted `已验证` label and `IntakeProbe.lean` provide no source or proof credit.

## Neighbor-target boundaries

| Target | Boundary |
|---|---|
| `THM-M-1481` simulated annealing | single-state temperature-scheduled stochastic search; not population selection/recombination |
| `THM-M-1483` particle swarm optimization | swarm velocity/position dynamics; not inherited genotype variation |
| `THM-M-1484` neural networks | model family rather than a genetic population-transition theorem |
| `THM-M-1485` backpropagation | gradient-based training algorithm with a different state and correctness contract |

## Formal and execution boundary

The canonical human statement and Lean expression remain null. No obligation registry or discovery
protocol is frozen, no formal candidate is credited, and no proof tree may be constructed from the
topic gloss. The first downstream task must select and review one source proposition before it can
freeze minimal imports, an elaborated expression, checked transports, and required mutations.
