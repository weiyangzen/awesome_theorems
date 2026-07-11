# Scope map

## Included claim

- A function field `K` of a curve over a characteristic-zero constant field.
- A smooth, projective, geometrically connected curve `X / K` with genus `g > 1`.
- A non-isotriviality hypothesis excluding curves descending to the constant field after the
  extension allowed by the selected source.
- Finiteness of the set `X(K)` of `K`-rational points.

## Decisions required at statement freeze

Primary-source inspection must freeze whether the constant field is algebraically closed (in
particular complex), the base curve is complete and nonsingular, and non-isotriviality means
nonconstant moduli, failure to become constant after finite extension, or another equivalent
condition. It must also freeze geometric-versus-arithmetic genus, separability, binder order,
universes, the encoding of rational points, and boundary cases: genus zero or one, constant curves,
empty rational-point sets, and finite constant-field extensions.

## Explicit exclusions

- Mordell/Faltings over number fields, the affine Mordell equation, or Mordell-Weil finite
  generation as substitutes.
- The false unrestricted assertion for isotrivial/constant curves over an infinite constant field.
- A bound on heights, degrees, or number of points when the source claim is only finiteness.
- A structure or hypothesis that assumes `Set.Finite (X(K))` and merely projects that field.
- The metadata label `已验证` as source or kernel evidence.

