# Scope map

## Included topic boundary

- A source-selected theorem connecting projective determinacy with a precisely stated large-cardinal
  hypothesis or inner-model conclusion.
- The exact ambient foundational theory and any model or consistency interpretation.
- The source's definition of projective pointclasses, games, strategies, determinacy, Woodin
  cardinals, and any measurable cardinal above them.
- The exact direction, quantifier order, cardinal count, and strength of the conclusion.

## Ambiguities to resolve at statement freeze

The repository phrase is compatible with materially different claims, including an implication
from specified Woodin-cardinal hypotheses to projective determinacy, a converse inner-model
consequence from projective determinacy, or an equiconsistency result. These differ in logical type
and cannot share a canonical Lean expression. Even within an implication, "large cardinals" does
not say whether there are finitely many, arbitrarily many, or infinitely many Woodin cardinals, or
whether a measurable cardinal above them is required. "Projective determinacy" may also mean the
full scheme or determinacy at one fixed projective level.

The statement phase must select an immutable source passage and freeze its object/metatheory
boundary, all ordered binders and hypotheses, the pointclass and game conventions, the exact
large-cardinal predicate, and whether the conclusion is truth in a universe, existence of an inner
model, relative consistency, or equiconsistency.

## Explicit exclusions

- The definition or existence of a Woodin cardinal by itself.
- Borel determinacy, the axiom of determinacy, or determinacy for only a convenient pointclass as a
  substitute for the selected projective-determinacy claim.
- An implication in the reverse direction, an equiconsistency, or an inner-model consequence when
  the source states another relationship.
- Replacing a quantified large-cardinal scheme with one assumed opaque proposition and proving a
  tautological projection.
- Treating mathlib's basic `Cardinal`, `Ordinal`, or `Set` APIs as encodings of Woodin cardinals or
  projective determinacy.
- The repository label `已验证` as human-source or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.

