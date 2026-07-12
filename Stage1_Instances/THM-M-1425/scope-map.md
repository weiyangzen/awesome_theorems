# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-1425`, the label `随机吸引子` (`random attractor`), the
collective attribution "many mathematicians", the period "twentieth century", and the gloss
`随机系统的吸引子` (`attractors of random systems`). Importance "high" and status `已验证` are
catalog metadata, not theorem or proof evidence. Intake preserves the broad subject of attractors
associated with random dynamics but does not expand the label into a theorem from memory.

## Proposition-changing decisions

An approved target correction must select an exact source proposition and freeze:

- the probability space, driving metric dynamical system or measurable base flow, time monoid or
  group, and whether null-set statements are completed or pointwise;
- the state space, topology or metric, compactness/completeness/separability assumptions, random
  cocycle or semiflow, continuity/measurability, and whether solutions are single-valued;
- the random-set encoding and its measurability: measurable graph, distance-function
  measurability, Effros/Borel hyperspace, or another source definition;
- pullback, forward, weak, local, global, uniform, or point attractor semantics, including the
  initial-family or universe class and basin;
- strict invariance equality versus forward inclusion, and whether it holds for all times and base
  points or only almost surely;
- the attraction distance or topology, one-sided versus symmetric Hausdorff distance, convergence
  mode, quantifier order, rate, and exceptional-set uniformity;
- compact absorbing-set, asymptotic-compactness, dissipativity, temperedness, continuity, order,
  contractivity, or other hypotheses; and
- whether the conclusion is existence, uniqueness, an omega-limit representation, minimality,
  robustness, upper semicontinuity, or singleton synchronization.

These choices yield inequivalent propositions. They are a resolution ledger, not a statement.

## Candidate families not credited

- Existence and uniqueness of a compact measurable pullback attractor from a compact absorbing
  random set plus pullback asymptotic compactness.
- Definition or construction of an attractor as a random omega-limit of an absorbing family.
- Forward or weak attraction, perhaps in probability rather than pathwise pullback convergence.
- Strict invariance, minimality, basin characterization, or independence from an absorbing set.
- Upper semicontinuity or robustness under a specified perturbation.
- A singleton random attractor obtained from synchronization or contraction.
- A multivalued random attractor for nonunique solutions.

No family in this list is selected or credited at intake.

## Explicit exclusions

Random dynamical systems (`THM-M-1424`) and multivalued random dynamical systems
(`THM-M-1426`) are neighboring roots, not substitutes. Coupling methods (`THM-M-1423`) may help
prove a synchronization or singleton-attractor result, but that does not identify this target. A
deterministic global attractor, ordinary omega-limit set, generic invariant set, or compactness and
Hausdorff-distance lemma cannot replace a source-selected random-attractor proposition.

Also excluded are structures that carry all desired attraction properties as fields, tautologies
that assume the conclusion, constant one-state examples, numerical sample paths, simulated
attractors, and unchecked convergence plots or certificates. The catalog label `已验证` supplies
neither human-source nor Lean kernel credit.

## Boundary cases

The selected source must decide empty and singleton random sets, zero noise, one-sided time,
noninvertible base motion, forward inclusion versus equality, pointwise versus almost-sure
invariance, local versus global basins, noncompact state spaces, infinite Hausdorff distance,
pseudometric zero, nonuniform exceptional sets, nonmeasurable hyperspaces, and nonunique dynamics.
Silently resolving any of these can materially change the proposition.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib provides generic APIs for flows and
invariant sets, omega-limit sets, compactness, Hausdorff distance, measurability, and filters. The
bounded intake search found no exact random-attractor, pullback-attractor, random-dynamical-system,
or random-set declaration in pinned mathlib. These APIs and the name search are discovery inputs
only, not an exhaustive anchor audit, statement elaboration, or proof evidence.
