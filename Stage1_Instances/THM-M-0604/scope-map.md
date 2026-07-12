# Scope map

## Included claim

- Bordism classes of closed finite-dimensional smooth manifolds, graded by dimension.
- Addition induced by disjoint union, with the empty manifold as additive identity and orientation
  reversal (or the characteristic-two unoriented convention) supplying additive inverses.
- Multiplication induced by Cartesian product, with the zero-dimensional point class as unit.
- Well-definedness of both operations with respect to bordism, associativity, distributivity, and
  the appropriate graded commutativity law.
- A single fixed tangential structure throughout the construction.

## Statement-phase decisions

The repository phrase does not identify the bordism theory. The statement phase must choose from
source evidence rather than conflate these alternatives:

| Decision | Alternatives requiring separation | Mathematical effect |
|---|---|---|
| Tangential structure | unoriented `O`, oriented `SO`, framed, spin, or another specified structure | changes the equivalence classes and coefficient ring |
| Commutativity | ordinary in the unoriented theory; signed/graded in the oriented theory | the factor-swap diffeomorphism changes product orientation by `(-1)^(mn)` |
| Representatives | manifolds embedded in a stable ambient space or abstract compact manifolds | changes the formal quotient interface, not automatically the theorem |
| Grading object | direct sum over `Nat` or a bundled graded object | determines the Lean carrier and binder shape |
| Equality mechanism | quotient by a proved equivalence relation or an equivalent geometric-homology model | requires a checked transport before either can receive credit for the other |

The exact primary source must also settle whether manifolds are required to be nonempty,
second-countable, boundaryless representatives, and which boundary/corner convention makes products
of bordisms legal. Dimension zero, the empty manifold, the point, disconnected representatives,
and products involving a zero class are mandatory boundary tests.

## Explicit exclusions

- A computation or presentation of a particular coefficient ring such as `MO_*` or `MSO_*`.
- Thom's classification of bordism groups by characteristic numbers.
- The h-cobordism or s-cobordism theorem.
- A ring structure postulated as fields of an abstract package rather than constructed on bordism
  classes with well-defined operations.
- A special-dimensional or homology-only surrogate for the graded geometric statement.

No repository-local Lean file for this target was located during intake. A later anchor audit must
search the pinned mathlib revision for concrete manifold-with-boundary, quotient, product,
orientation, and bordism infrastructure before fixing the formal expression.
