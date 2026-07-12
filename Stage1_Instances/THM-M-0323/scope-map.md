# Scope map

## Frozen repository input

The source inventory names `THM-M-0323` "Schauder basis theorem", attributes it to Juliusz
Schauder, dates it to 1927, and describes it only as "existence of a basis in Banach spaces". That
phrase omits the Banach space, scalar field, topology/norm, index order, and meaning of "basis".

## Ambiguity that blocks an exact claim

A Schauder basis is a sequence whose partial-sum expansions converge in norm, with unique
coordinates. It is not the algebraic Hamel basis whose existence follows from choice. The literal
phrase also cannot mean that every Banach space has a Schauder basis: the repository's adjacent
Enflo target records the contrary theorem, and nonseparable Banach spaces already cannot have a
countable norm-dense Schauder basis.

The statement phase must select one source-backed proposition. Current candidates are:

1. the Haar system, in a source-specified ordering and normalization, is a Schauder basis for a
   specified function space such as `L^p[0,1]` in the source's allowed range; or
2. the Faber-Schauder system is a Schauder basis for a specified continuous-function space; or
3. another exact existence theorem explicitly located in Schauder's primary text.

These candidates are not interchangeable and receive no statement credit at intake.

## Required statement decisions

- Real or complex scalars and the precise normed complete space.
- Haar versus Faber-Schauder system, normalization, enumeration, and endpoint conventions.
- Whether the conclusion supplies basis vectors plus continuous coordinate functionals, uniqueness,
  or merely convergence/density.
- The precise `p` range and treatment of `p = 1`, `p = 2`, and endpoints if an `L^p` theorem is used.
- Zero/trivial space, finite-dimensional cases, separability assumptions, and index starting point.
- The relationship to mathlib's `SchauderBasis`, whose expansion uses conditional partial sums.

## Explicit exclusions

- "Every Banach space has a Schauder basis."
- Existence of a Hamel basis as a substitute for a Schauder basis.
- The mere definition `SchauderBasis`, or a structure taking a desired basis as input.
- `RankOneDecomposition.basis` without proving that the target function space has the required
  sequence of projections.
- Results about Schauder fixed points, Schauder estimates, or arbitrary topological filter bases.
