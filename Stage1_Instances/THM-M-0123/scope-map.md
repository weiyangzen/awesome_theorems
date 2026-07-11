# Scope map

## Included root claim

- Base: every number field `K`.
- Object: a smooth, proper, geometrically connected curve `X / K`.
- Genus boundary: `g(X) >= 2`.
- Conclusion: the `K`-rational points of `X` form a finite set/type.
- Intended Lean point model: sections `Spec K -> X` of the structure map;
  equivalence to any chosen functor-of-points encoding must be checked.

The statement node must decide the precise scheme/curve package, whether
geometric connectedness is part of the curve convention, the native genus
definition, universe levels, ordered binders, and `Finite` versus `Set.Finite`
encoding. It must freeze the toolchain and imports before exactness is claimed.

## Explicit exclusions

- Mordell-Weil finite generation for abelian varieties or elliptic curves.
- Effective bounds, uniform boundedness, and the uniform Mordell conjecture.
- Curves of genus zero or one.
- A special case over `Q` in place of arbitrary number fields.
- Finiteness of points of bounded height in place of finiteness of all rational
  points.
- A supplied abstract `genusAtLeastTwo : Prop` as proof that the actual curve
  has genus at least two.

## Required transports and mutations

Later encodings must check the transport between section-valued rational points
and `X(K)`, and between any native genus predicate and `2 <= genus X`. Statement
mutation tests must reject removal of properness, smoothness, geometric
connectedness where required by the selected convention, the number-field
hypothesis, or the genus bound. They must also reject weakening the conclusion
to bounded-height finiteness and test genus `0`, `1`, and exactly `2`.

