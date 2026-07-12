# Scope map

## Included theorem family

- An autonomous vector field on a source-specified planar domain.
- A scalar Dulac multiplier with exactly the regularity demanded by the selected source.
- A source-specified one-sign condition on the divergence of the multiplied vector field.
- A conclusion excluding the source's precise notion of nonconstant periodic orbit or limit cycle.
- The Green/divergence argument only after curve regularity, enclosed-region hypotheses, orientation,
  and the required integral theorem have exact checked interfaces.

## Ambiguities to resolve at statement freeze

The repository wording does not determine:

1. Whether the domain is open, connected, simply connected, or has finite connectivity.
2. Whether the vector field and multiplier are `C1`, differentiable with continuous partials, or
   satisfy a weaker almost-everywhere condition.
3. Whether divergence is strictly positive/negative everywhere, weakly one-signed and not
   identically zero, or permitted to vanish on a measure-zero set.
4. Whether solutions are maximal ODE solutions, a global flow, or regular parametrized closed
   trajectories, and what uniqueness hypotheses are assumed.
5. Whether the conclusion excludes all periodic orbits, only regular limit cycles, or bounds their
   number by the connectivity of the domain.
6. Whether equilibrium trajectories count as periodic and how boundary-touching curves are treated.

## Explicit exclusions

- The elementary Bendixson criterion with multiplier `B = 1` as an automatic substitute for the
  more general Bendixson-Dulac criterion.
- Poincare-Bendixson classification, uniqueness or stability of a limit cycle, or a numerical phase
  portrait as a substitute for nonexistence.
- A tautological statement assuming directly that no periodic orbit exists.
- A rectangular divergence theorem alone as proof of the criterion without the checked passage
  from a periodic trajectory to its enclosed region and boundary integral.
- The repository's `verified` label as evidence of a primary proof or Lean kernel closure.

No canonical Lean target is frozen at intake because no exact source theorem has been selected.
