# Scope map

## Included claim

- The Hasse-Weil zeta function formed from point counts over finite extensions of a finite base
  field.
- A smooth projective algebraic variety over that field, with dimension and connectedness
  conventions to be taken from the selected primary statement.
- The standard Weil-conjectures package: rationality; the duality functional equation; factor
  degrees governed by cohomological Betti numbers; and reciprocal-root weights/absolute values.
- All four components as separately visible formal obligations. Proving only rationality or only
  the top-weight estimate cannot close the package.

## Decisions required at the statement gate

The source audit must freeze the meaning of "variety" (scheme versus a narrower classical
encoding), finite-field cardinality notation, geometric connectedness, dimension and purity,
closed-point Euler product versus exponential point-count series, signs and powers in the
functional equation, indexing of the cohomological factors, the chosen embedding into `C`, and
whether integer coefficients are a separate assertion. It must also decide how empty,
zero-dimensional, disconnected, and non-geometrically-connected cases are represented.

Ordered binders, universes, explicit hypotheses, minimal imports, foundation/choice profile, and
checked transports between equivalent zeta-function encodings belong to the statement phase. No
abstract record may assume the four conclusions as fields merely to manufacture an easy theorem.

## Explicit exclusions

- The unrelated Weil conjecture on Tamagawa numbers, the Weil representation, Weil divisors, or
  Weil's criterion.
- The zeta function of only a single curve, projective space, elliptic curve, or finite set as a
  substitute for the variety-level theorem.
- Rationality alone (Dwork), the functional equation alone, or only Deligne's weight bound.
- A generic polynomial factorization statement with the geometric/cohomological content erased.
- The adjacent `THM-M-0192` Deligne-theorem dossier as interchangeable proof or scope authority.

The first downstream blocker is a pinpoint, edition-stable source statement whose assumptions and
normalizations can be mapped without broadening or silently selecting a special case.
