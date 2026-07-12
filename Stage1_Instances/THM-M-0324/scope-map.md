# Scope map

## Frozen repository input

The target manifest identifies `THM-M-0324` as Enflo's theorem in functional analysis, rank 820,
with uniform `L0 / rework_required` status. Stage0 supplies Per Enflo, 1973, and only the phrase
"Banach spaces need not have a basis." Its `verified` label is explicitly untrusted under rev-5.6.

## Canonical human scope

The intake freezes the conservative theorem family:

> There exists a Banach space over the real or complex scalars which has no Schauder basis.

"Basis" means a countable Schauder basis: vectors with continuous coordinate functionals whose
ordered partial sums converge in norm to every vector. It does not mean a Hamel basis. Enflo's
primary construction is stronger: a separable reflexive Banach space failing the approximation
property. A space with a Schauder basis has uniformly bounded finite-rank partial-sum projections
converging pointwise to the identity, hence has the bounded approximation property. That bridge
explains the catalog summary but receives no proof or H0 credit at intake.

## Decisions deferred to the statement phase

- Whether the root is formalized over `Real`, `Complex`, or with a checked scalar-extension bridge.
- The precise existential packaging of a type together with its normed-space and complete-space
  instances, without leaking typeclass metavariables.
- Whether separability and reflexivity belong in the canonical root or in a stronger alternate.
- The exact Lean definition of the approximation property, finite rank, and convergence topology.
- The exact primary Theorem 1 statement and the source steps deriving no Schauder basis.
- Foundation and choice requirements for the constructed space and any completion/quotient.

## Explicit exclusions

- A Hamel-basis nonexistence claim, which would change the mathematics and conflict with choice.
- A nonseparable Banach space with no countable dense sequence; that is an easier cardinality
  obstruction, not Enflo's theorem.
- Merely proving that a particular sequence is not a basis.
- Absence only of an unconditional basis or of a basis with a specified basis constant.
- Failure of the approximation property asserted as an axiom or custom predicate with no Enflo
  construction.
- A finite-dimensional, zero-space, or incomplete normed-space surrogate.

## Lean representation boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Analysis.Normed.Module.Bases` defines `SchauderBasis`, `SchauderBasis.proj`,
`SchauderBasis.tendsto_proj`, `SchauderBasis.finrank_range_proj`, and
`SchauderBasis.exists_norm_proj_le`. These APIs cover the basis-to-projection side of the intended
bridge. The limited intake search found no general approximation-property predicate and no Enflo
counterexample construction in pinned mathlib. A full candidate audit belongs to the later
`ANCHOR_AUDIT` node. This representation inventory supplies no theorem completion evidence.
