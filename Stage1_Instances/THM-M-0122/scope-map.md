# Scope map

## Included claim

The target is the number-field Mordell conjecture proved by Faltings. For a
number field `K` and a smooth, projective, geometrically connected curve `C`
over `K`, geometric genus greater than one implies that `C(K)` is finite.

The statement phase must expose the field and number-field structure, the
scheme and structure morphism, relative dimension one, smoothness,
projectivity/properness, the selected geometric connectedness or integrality
condition, a native geometric-genus invariant, and the rational-point type.
Universes and ordered binders must be explicit.

## Exclusions

- Faltings' isogeny and Shafarevich finiteness theorems.
- Mordell-Weil finite generation, Siegel's theorem, or function-field Mordell.
- Higher-dimensional generalizations and arbitrary finitely generated fields.
- A supplied finite set, a finite-type hypothesis, or a wrapper implication as
  a substitute for proving finiteness of all rational points.
- A free natural-number parameter called genus without a checked connection to
  the curve's geometric genus.
- Properness as an unproved substitute for projectivity, or geometric
  integrality as an unproved substitute for the chosen curve convention.

## Required transports

The section encoding of `K`-points and a slice/functor-of-points encoding must
be related by checked equivalence before finiteness is transported. Any use of
a regular proper model or a different curve convention requires checked
existence and equivalence bridges. The `g > 1` and `g >= 2` forms may be
transported only after genus is tied to the curve.

## Statement mutation obligations

Reject mutations dropping the number-field assumption, smoothness,
projectivity, the geometric connectedness/integrality condition, or the genus
bound. Reject conclusions that establish only finite generation, bounded
height, or finiteness of a selected subset. Test genus zero and one explicitly:
they demonstrate why the strict genus boundary cannot be removed.
