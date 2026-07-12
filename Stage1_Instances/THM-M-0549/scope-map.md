# Scope map

## Included claim

- Ordinary singular cohomology of a topological space `X` with coefficients in a commutative ring
  `R`.
- The degree-additive map `H^p(X; R) x H^q(X; R) -> H^(p+q)(X; R)` induced by the cochain cup
  product (equivalently, by a chain-level diagonal approximation after conventions are fixed).
- Associativity and a degree-zero unit on cohomology.
- Graded commutativity for homogeneous classes with the Koszul sign `(-1)^(p*q)`.
- Naturality under pullback along continuous maps.

These clauses state the theorem family meant by the source phrase "the structure of the cohomology
ring". They do not yet choose one Lean conjunction or bundled graded-ring isomorphism as the
canonical formal target.

## Statement-phase decisions

The statement phase must inspect and select an exact source theorem before fixing:

- the class of spaces and whether singular, simplicial, or cellular cohomology is primary;
- the precise coefficient ring assumptions, left/right conventions, and tensor identifications;
- unreduced versus reduced cohomology and the treatment of degree zero and the empty space;
- natural-number versus integer grading and the representation of the sign;
- whether naturality, associativity, unit, and graded commutativity are one bundled root or separately
  composed obligations;
- binder order, universes, typeclass assumptions, minimal imports, and the foundation profile.

Degenerate cases such as the zero coefficient ring, empty `X`, negative degrees in an integer-graded
encoding, and characteristics two must be preserved or explicitly excluded by the chosen source.

## Explicit exclusions

- Merely defining a `cupProduct` field or assuming the ring laws in a structure.
- A theorem about an arbitrary pre-existing graded-commutative ring with no construction from
  singular cochains.
- Only the bilinear pairing, without the laws needed for the stated cohomology-ring structure.
- The cap product, intersection product, Steenrod operations, or a characteristic-class formula as
  a substitute.
- A computation of the cohomology ring of one particular space as a substitute for the general
  structural theorem.

## Formalization boundary

Repository search found cup-product mentions in adjacent historical Stage1 files, including
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_107.lean`, but those files describe a missing API or
package an operation as data. They are discovery inputs only and give this target no statement or
proof credit. The anchor-audit phase must search the pinned mathlib tree and external Lean projects
against the exact statement, rather than inheriting that historical assessment.
