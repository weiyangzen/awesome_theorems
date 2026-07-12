# Scope map

## Included topic boundary

- An imaginary quadratic field, or an order in one, selected by an exact source.
- Complex multiplication of a lattice or elliptic curve and the relevant endomorphism order.
- The modular function or CM value used by the selected theorem.
- The Hilbert class field or ring class field and the exact generation or reciprocity conclusion.
- All conductor, discriminant, embedding, integrality, and normalization assumptions required by the
  selected statement.

## Ambiguities to resolve at statement freeze

The repository record is compatible with several non-interchangeable targets:

1. A first-main-theorem formulation asserting algebraicity of a singular modulus and generation of
   a Hilbert class field over an imaginary quadratic field.
2. The corresponding ring-class-field theorem for an order of conductor greater than one.
3. A second-main-theorem or Shimura-reciprocity formulation describing the Artin/Galois action on
   CM values.
4. An existence or classification theorem for elliptic curves with complex multiplication.

The statement phase must select an immutable source passage and freeze its ordered binders,
definitions, exact class field, modular invariant, hypotheses, conclusion, and normalization. It
must decide maximal versus nonmaximal order, conductor and discriminant conventions, the chosen
complex embedding, and exceptional unit cases.

## Explicit exclusions

- The entire subject of complex multiplication packaged as though it were one proposition.
- `NumberField.IsCMField` or a theorem about CM number fields as a substitute. In mathlib this
  predicate concerns a totally complex quadratic extension of its maximal real subfield; it does
  not state the class-field-generation theorem for imaginary quadratic fields.
- Positivity or finiteness of a class number as a substitute for construction of a class field.
- A theorem about elliptic-curve Weierstrass models absent the CM and class-field conclusion.
- Kronecker's Jugendtraum (`THM-M-0515`) or Shimura reciprocity (`THM-M-0513`) silently merged into
  this target; adjacent repository entries are separate targets.
- A definition packaged as assumed data followed by a tautological projection.
- The inventory label `已验证` as evidence of a human proof or Lean closure.

No canonical Lean target is frozen at intake because the source record does not identify one.
