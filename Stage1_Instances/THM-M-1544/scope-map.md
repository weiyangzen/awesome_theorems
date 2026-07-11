# Scope map

## Included claim

- A fixed instanton number (second Chern number/charge) and an explicitly chosen compact gauge
  group, initially expected to be the original rank-two case.
- Framed anti-self-dual connections on `S^4` (equivalently suitably framed finite-action
  instantons on `R^4` after the conformal identification), modulo framed gauge equivalence.
- Finite-dimensional ADHM linear data satisfying both the ADHM equations and the appropriate
  stability/nondegeneracy condition, modulo the corresponding change-of-basis group.
- Both directions: reconstruction of an instanton from admissible data and recovery/classification
  of instantons by such data, including equivalence compatibility.

## Decisions required by the statement phase

Primary-source inspection must freeze the gauge group (`SU(2)`, `U(r)`, or another classical
variant), charge sign and positivity, framing point, regularity class of connections and gauge
maps, real/quaternionic versus complex matrix presentation, moment-map equations, stability or
costability hypotheses, quotient group, and whether the result is a bijection of sets or an
isomorphism/diffeomorphism of moduli spaces. It must also settle charge zero and empty-moduli
boundary cases and fix ordered binders and universes.

## Explicit exclusions

- Merely proving that a displayed tuple satisfies the algebraic ADHM equations.
- Only constructing a connection without anti-self-duality, regularity, charge, or completeness.
- A one-way map from ADHM data to instantons presented as the full classification.
- Substituting the Nahm transform, Donaldson's theorem, or a generic quotient existence theorem.
- Encoding the desired correspondence as a structure field or hypothesis.

The formal target will require substantial bundle, connection, curvature, elliptic-analysis, and
quotient infrastructure. Missing APIs must be reported rather than abstracted into the conclusion.
