# Source-statement crosswalk

## Selected statement

The intake selected the classical algebraic-curve divisor formula:

`ell(D) - ell(K_X - D) = deg(D) + 1 - g(X)`

for every divisor `D` on a smooth projective geometrically integral curve `X`
over an arbitrary field `k`, where `K_X` is canonical and
`ell(E) = dim_k H^0(X, O_X(E))`. `Statement.lean` preserves that scope rather
than the legacy existential statement shape.

## Source boundary

Robin Hartshorne, *Algebraic Geometry* (1977), Chapter IV, Section 1, Theorem
1.3 remains the intake's primary-source candidate. This phase does not promote
that lead to `H0`: the immutable edition/page packet, incorporated definitions,
errata check, arbitrary-field/geometric-integrality convention bridge, and
independent review remain for `ANCHOR_AUDIT`.

| Mathematical component | Lean encoding | Boundary |
|---|---|---|
| field `k` | `[Field k]` | arbitrary field; not silently specialized |
| curve `X/k` | `CurveOver k` | scheme plus its structure morphism |
| smooth dimension one | `SmoothOfRelativeDimension 1` | concrete pinned predicate |
| projective | `IsProper` | properness is the available statement-level encoding; projective/proper comparison remains source debt |
| geometrically integral | `GeometricallyIntegral` | concrete pinned predicate |
| divisors and subtraction | `RiemannRochData.Divisor`, `sub` | conclusion-free typed interface plus semantic compatibility predicates |
| `deg`, `ell`, `K_X`, genus | `degree`, `ell`, `canonicalDivisor`, `genus` | compatibility predicates require the standard meanings; concrete native transports remain downstream debt |
| formula for every `D` | `RiemannRochTarget` | universal divisor binder and integer equality |

The compatibility predicates do not include the formula and cannot prove it
definitionally. The target quantifies over every compatible realization, so it
does not existentially choose convenient data or accept a caller-supplied
equality.

## Alternate and mutation boundary

`riemannRochTarget_iff_expanded` is the only credited alternate encoding and
is checked by `Iff.rfl`. The removed-geometric-integrality, rational-field-only,
existential-divisor-binder, and canonical-divisor-only propositions are
separately elaborated mutations. Each is rejected as the canonical type.

This crosswalk supports exact statement identity only. It supplies no proof of
Riemann-Roch, no primary-source acceptance, no native divisor API transport, no
parent acceptance, and no `AUDIT-Z` or `THEOREM-Z` decision.
