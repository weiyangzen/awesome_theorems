# Scope map

## Included claim

- An arbitrary locally small category `C`, with universe levels made explicit during statement work.
- Objects `X Y : C` and contravariant representables `Hom(-, X)` and `Hom(-, Y)`.
- Both directions of `Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y)`.
- The element-level natural bijection `Nat(Hom(-, X), F) ≅ F(X)` as the mathematical bridge
  explaining reflection of object isomorphisms.

## Statement-phase decisions

Freeze universe levels, the exact local-smallness encoding, `Type` versus bundled hom targets,
variance/opposite-category notation, and whether the canonical expression uses `Nonempty` or an
explicit map from a functor isomorphism to an object isomorphism. Binder order must be recorded.
Degenerate categories and `X = Y` require no extra assumptions.

## Exclusions

- The covariant Yoneda lemma without a checked variance transport.
- Representability criteria, density, enriched Yoneda, or homological exactness as substitutes.
- Equality of objects or mere equivalence of hom-set cardinalities in place of isomorphism.
- Collateral preadditive, derived, long-exact, or spectral-sequence APIs from the legacy module.

The legacy `S1_M_138.lean` object-isomorphism wrapper matches the intended shape but remains
unaccepted discovery evidence until the later statement and anchor-audit nodes re-elaborate and
audit it under rev-5.6.

