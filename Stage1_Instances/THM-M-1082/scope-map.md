# Scope map

## Included theorem family

- A stochastic process `X : T -> Omega -> E` on a probability space, with arbitrary index type
  unless the selected source imposes additional structure.
- Gaussianity tested on every finite set or finite tuple of indices through the corresponding
  finite-dimensional random vector.
- The standard real-valued alternate formulation in which every finite linear combination of
  coordinates is a (possibly degenerate) real Gaussian random variable.
- A checked relationship between the finite-dimensional-law and linear-combination formulations,
  if both are credited by the final statement.

## Statement-phase decisions

The selected pinpoint source must fix whether `E` is `R`, `R^d`, or a real topological vector
space; whether zero-variance Gaussian laws count; whether the probability measure is explicit;
whether coordinate measurability is included or follows from Gaussian-law hypotheses; and whether
the named result is a definition, an equivalence theorem, or a preservation theorem. The formal
statement must then freeze ordered binders, universes, measurable/topological structures, finite
index encoding, and all typeclass assumptions.

The present source phrase, "the theory of Gaussian processes", is not itself proposition-shaped.
Consequently intake freezes only this theorem family and records the missing unique proposition as
the first downstream blocker rather than inventing a broader result.

## Explicit exclusions

- Existence of a process from a positive-semidefinite covariance kernel.
- Classification by mean and covariance, sample-path continuity, or a Karhunen-Loeve expansion.
- Bounds or comparison results such as Dudley, Slepian, Sudakov, Fernique, or Borell-TIS, which have
  separate target IDs in the manifest.
- Brownian motion, stationarity, centeredness, independence, or continuity as implicit hypotheses.
- Assuming an abstract predicate whose fields already contain a distinct desired conclusion and
  presenting a projection as proof of that conclusion.

No downstream proof may substitute one excluded theorem for the finite-dimensional Gaussianity
characterization selected here.
