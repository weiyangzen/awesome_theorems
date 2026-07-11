# Scope map

## Included theorem family

- A commutative diagram with two rows of five objects and four horizontal morphisms.
- Exactness of both rows at the positions required by the chosen categorical formulation.
- Vertical morphisms from the upper row to the lower row.
- Standard outer hypotheses: the first vertical map is epic, the second and fourth are
  isomorphisms, and the fifth is monic.
- The conclusion that the middle (third) vertical morphism is an isomorphism.

The anticipated ambient setting is an abelian category. This covers the classical module and
abelian-group versions without choosing either concrete category as the canonical root.

## Boundaries to freeze at statement phase

The exact source edition and theorem label, diagram orientation, required exactness positions,
zero-object endpoints (if any), and whether the source states the result in an abelian category or
only for modules/abelian groups must be fixed before canonicalization. Lean universes, ordered
binders, `ComposableArrows` indexing, imports, declaration type, environment fingerprint,
degenerate cases, and transports to concrete categories also remain open.

## Explicit exclusions

- The four lemma, short five lemma, snake lemma, nine lemma, or a long-exact-sequence consequence.
- A statement assuming the middle morphism is an isomorphism or replacing exactness by an opaque
  predicate whose needed consequence is supplied as a hypothesis.
- Only injectivity or only surjectivity of the middle map.
- The legacy wrapper in `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_097.lean` as accepted
  rev-5.6 proof or statement evidence.

The source metadata's `已验证` label is untrusted and supplies no machine-proof credit.
