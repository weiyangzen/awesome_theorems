# Scope map

## Included claim

- The classical real-variable Hardy space `H^1(R^n)`, not a holomorphic Hardy space.
- `BMO(R^n)` defined by uniformly bounded mean oscillation over cubes or balls.
- The quotient of `BMO` by almost-everywhere constant functions, since constants vanish in the
  pairing with the relevant zero-mean Hardy-space inputs.
- The pairing `f, b -> integral f(x) b(x) dx`, first interpreted where it is well-defined and then
  extended continuously.
- Both directions: a BMO class induces a bounded functional, and every bounded functional on
  `H^1` is represented by a BMO class.
- A topological linear equivalence with two-sided norm bounds. Isometry is not included unless the
  selected normalizations and primary source establish it.

## Decisions reserved for the statement phase

The selected source must fix `n >= 1`, real versus complex scalars, Lebesgue measure, balls versus
cubes, the maximal-function or atomic model of `H^1`, the BMO seminorm and quotient norm, and the
precise dense domain used to define the pairing. The statement must also decide whether the result
is packaged as a continuous linear equivalence, a representation theorem plus uniqueness modulo
constants, or mutually inverse maps with explicit constants.

Boundary cases requiring explicit treatment include dimension zero, infinite or undefined
pairings for arbitrary representatives, equality only almost everywhere, choice of BMO
representative, and the zero functional. Binder order, universes, measurability, integrability,
scalar restriction, and completeness assumptions remain open until these choices are frozen.

## Explicit exclusions

- The tautology that the Banach dual of an abstract type named `H1` is another abstract type named
  `BMO`.
- A structure that assumes the desired equivalence or representation theorem as a field.
- Only the easy direction from BMO to bounded functionals, or only the converse representation
  direction.
- The John-Nirenberg inequality, atomic decomposition of `H^1`, `H^p` duality for `p != 1`, a
  martingale BMO theorem, or a bounded-domain variant as a substitute for the Euclidean theorem.
- Equality of raw BMO functions rather than uniqueness modulo almost-everywhere constants.

The future Lean target must use concrete measure-theoretic, seminormed/quotient, integration, and
continuous-linear-map interfaces, or record a precise missing-API blocker. No broadened abstract
interface receives statement or proof credit.
