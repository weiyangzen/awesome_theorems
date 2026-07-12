# Scope map

## Included result family

- A source-specified real-variable Hardy space `H^1` on a fixed underlying space and measure.
- A source-specified atom class, including support, cancellation, measurability, and size conditions.
- Representation of every `H^1` element by an absolutely summable family of scalar multiples of
  atoms, with a precisely stated convergence mode.
- The converse inclusion and quantitative comparison between the `H^1` norm and the infimum of
  coefficient `l^1` sums, if these are part of the reviewed source theorem.

## Ambiguities to resolve at statement freeze

The repository record does not decide the following material choices:

1. Whether `H^1` is the real Hardy space on `R^n`, an analytic Hardy space, a boundary space, or a
   Hardy space over another metric-measure structure.
2. Whether the Hardy norm is defined by a radial maximal function, nontangential maximal function,
   grand maximal function, square function, or another source-proved equivalent norm.
3. Whether atoms are supported on balls or cubes; use an `L-infinity`, `L^2`, or general `L^q`
   size bound; and require integral zero or higher moment cancellation.
4. Whether the theorem includes both directions, equality of spaces, equivalence of norms, exact
   constants or existential constants, and which topology or almost-everywhere sense governs the
   countable sum.

The statement phase must inspect an immutable primary source and freeze these decisions, ordered
binders, constants, boundary cases, and scalar convention before defining a Lean target.

## Explicit exclusions

- Atomic decompositions of Banach spaces, operator algebras, Besov/Triebel-Lizorkin spaces, or
  martingale Hardy spaces as substitutes.
- A finite linear-span density theorem as a substitute for a countable atomic representation.
- An `L^1` decomposition that omits the defining Hardy-space condition.
- A theorem assuming the desired atomic representation as a structure field and returning it.
- The repository label `已验证` or the intake API probe as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not uniquely determine
a mathematical proposition and pinned mathlib does not itself supply the missing Hardy/atom choices.

