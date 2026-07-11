# Scope map

## Included claim

- A time-homogeneous transition semigroup on a topological measurable state space.
- The Markov, positivity/probability-preserving, semigroup, Feller continuity, and strong
  continuity assumptions required by the selected source.
- Existence of a probability-space/path-space realization with the supplied transition laws and
  the Markov property.
- Right-continuous or cadlag paths only if the chosen source theorem proves that conclusion under
  the frozen hypotheses.

## Boundary decisions for the statement phase

Primary-source inspection must fix whether the state space is locally compact, second countable,
Hausdorff, Polish, or a more general Borel space; whether `C₀(E)` or bounded continuous functions
carry the Feller action; whether the semigroup is conservative; and whether existence is for each
starting point, every initial distribution, or one supplied sample space. It must also decide time
indexing, measurability of the process, canonical path space, right continuity versus cadlag paths,
explosion/cemetery-state behavior, and the zero-time and empty-state edge cases.

## Explicit exclusions

- Defining a `FellerProcessRealization` whose fields assume the desired Markov and transition-law
  conclusions.
- A finite-state or discrete-time Markov-chain existence theorem substituted for the general
  Feller-process claim.
- Invariance, ergodicity, generator characterization, Dynkin's formula, or continuous sample paths
  unless they are part of the selected source theorem.
- Treating kernel integrability wrappers in the legacy module as terminal existence evidence.

The statement phase must use concrete mathlib objects or record exact missing APIs. No stronger
topology or weaker conclusion may be chosen merely to obtain elaboration.
