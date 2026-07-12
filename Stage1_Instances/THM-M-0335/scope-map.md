# Scope map

## Included claim

- An inclusion `N subset M` of type `II_1` factors, with inclusion conventions taken from the
  selected primary theorem.
- The Jones index `[M:N]`, not a group index, polynomial index, Fredholm index, or categorical
  dimension merely renamed as the target.
- The discrete restriction below `4`: `[M:N] = 4 cos^2(pi/n)` for an integer `n >= 3`.
- The conventional combined value set consisting of those discrete values and the continuous range
  at least `4`, subject to source verification of whether the theorem asserts necessity only or
  realization as well.

## Boundary decisions for statement freeze

The statement phase must decide from the primary text: concrete versus abstract factors; the exact
definition of type `II_1`, subfactor, trace, dimension, and index; whether the inclusion must be
proper; whether infinity is in the codomain; whether index `1`/`n=3` is retained; and whether the
claimed theorem is only the restriction on possible indices or also existence of inclusions for
every listed value. It must preserve exact equality rather than numerical cosine approximations.

The Lean encoding also needs a universe and representation decision for `N` and `M`, an inclusion
map with all required continuity/normality properties, factor and finite-trace predicates, an index
valued in a source-faithful type, and exact real trigonometry. These cannot be replaced by assumed
structure fields containing the desired classification.

## Explicit exclusions

- The Jones polynomial, Temperley-Lieb algebra classification, principal graph restrictions, or
  knot invariants as substitutes for the index-value theorem.
- Finite group subgroup indices or finite-dimensional algebra dimension ratios alone.
- A theorem only about von Neumann algebras, double commutants, or star subalgebras without the
  type `II_1` factor inclusion and Jones index.
- A finite sample of values, a floating-point computation, or only the easy inequality branch.
- The manifest label `已验证` as human-source or machine-proof evidence.

No canonical Lean proposition is frozen at intake because the pinned library probe did not locate
the required subfactor-index interfaces and the exact primary-source boundary remains under review.

