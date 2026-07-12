# Scope map

## Provisional included claim

- A concrete first-order formulation of Zermelo-Fraenkel set theory without Choice.
- A concrete sentence or axiom scheme expressing the generalized continuum hypothesis.
- Relative consistency in a source-faithful semantic or syntactic sense.
- Godel's constructible-universe route: from a model of ZF, obtain an inner model `L` satisfying
  ZF and GCH, with every transfer needed for the selected consistency conclusion.

## Decisions required at statement freeze

The next phase must inspect an immutable source and freeze whether `Con(T)` means model existence,
absence of a derivation of falsity, or a checked equivalence between those forms. It must select the
language and deductive calculus; set-theory axiom schemas and their coding; the exact formulation of
ZF (not ZFC); GCH at all infinite cardinals; the model and inner-model notion; universe levels; and
the ordered quantifiers. It must say whether the theorem assumes a set model of ZF, how `L` is
constructed inside possibly nonstandard models, and which metatheory supplies completeness or
soundness transfers.

Boundary cases include empty carriers, inconsistent theories, nonstandard models, proper-class
versus set-sized constructions, and the distinction between external ambient cardinals and the
cardinals computed by the inner model.

## Explicit exclusions

- The continuum hypothesis alone instead of GCH.
- The forcing result that CH or GCH can fail, or the combined independence theorem.
- A proof that GCH implies CH, or a bare cardinal identity such as `2 ^ aleph_0 = aleph_1`.
- Mathlib's `ZFSet`, whose module explicitly models ZFC using Lean's choice, as a substitute for a
  first-order relative-consistency proof from ZF.
- A structure that assumes the desired inner model or consistency conclusion as a field.
- The inventory label `已验证` as human-proof or kernel evidence.

No canonical Lean target is frozen during intake.
