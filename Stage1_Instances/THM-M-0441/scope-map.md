# Scope map

## Included subject boundary

- A fixed o-minimal structure expanding the ordered real field, and a set definable in that
  structure, with parameters handled exactly as the selected source states.
- Rational points in affine space, a fixed multiplicative/projective height convention, and the
  bounded-height counting function.
- The algebraic part of the definable set, formed from connected positive-dimensional
  semialgebraic subsets, and the complementary transcendental part.
- The uniform bound `N(X - X_alg, T) <= c(X, epsilon) * T^epsilon` (or the exact source-equivalent
  notation), with every quantifier and threshold frozen from the primary source.

## Decisions required at statement phase

The statement phase must inspect a stable copy of the primary paper and freeze: theorem label and
pages; ambient dimension; definability with or without parameters; whether the structure expands
the real field or a more general ordered field; affine versus projective height; `T`'s domain and
lower bound; the precise algebraic-part definition; dependence of the constant; and strict versus
nonstrict inequalities. It must also record degenerate cases such as dimension zero, empty sets,
`epsilon <= 0`, and small height bounds.

## Explicit exclusions

- Wilkie's earlier conjecture or stronger polylogarithmic bounds for restricted exponential
  structures.
- The block/family refinements sometimes also called Pila-Wilkie, or counting algebraic points of
  bounded degree, unless the pinpoint source proves that this metadata names one of them.
- Replacing o-minimality, algebraic part, height, or the asymptotic conclusion by unconstrained
  predicate/data fields.
- Treating finite empty/universal-set wrappers in the legacy Lean file as proof credit for the root.

Later nodes must freeze universes, imports, declaration type, expression/environment fingerprint,
checked transports, hypothesis mutations, and the complete obligation and trust graphs.
