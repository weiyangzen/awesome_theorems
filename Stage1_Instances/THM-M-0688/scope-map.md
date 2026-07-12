# Scope map

## Included topic boundary

- A source-specified, syntactic ordinal notation system.
- Its represented ordinal domain and exact upper bound or coverage claim.
- A semantics from notations to ordinals, or an intrinsic order with a source-specified adequacy
  relation.
- The concrete theorem asserted about the system: for example normalization, comparison
  correctness, representability, well-foundedness, or effectiveness.
- All hypotheses and conventions required by the selected source.

## Ambiguities to resolve at statement freeze

The repository record does not decide among materially different possible targets:

1. Cantor normal-form notations for ordinals below epsilon-zero, with arithmetic correctness.
2. A Veblen hierarchy or a notation system reaching Gamma-zero.
3. A stronger collapsing-function system for a larger proof-theoretic ordinal.
4. An abstract existence, coding, order-type, well-foundedness, or computability theorem about a
   source-defined notation system.

The statement phase must inspect an immutable source and freeze one proposition, including the
ordinal boundary, syntax, equality convention, semantics, ordered binders, hypotheses, and exact
conclusion. It must decide whether every ordinal below the boundary is represented, whether
representations are unique or normalized, whether comparison is decidable and order-reflecting,
whether fundamental sequences are part of the claim, and whether well-foundedness is external or
proved for a recursive relation.

## Explicit exclusions

- Mathlib's `ONote` or `NONote` merely because it is locally available, absent a checked source
  identifying epsilon-zero and the corresponding theorem.
- Veblen functions, Cantor normal form, ordinal arithmetic, transfinite induction, or ordinal
  analysis as substitutes for a theorem specifically about a notation system.
- Replacing "large ordinals" by an arbitrary convenient bound such as epsilon-zero or Gamma-zero.
- A structure carrying its desired correctness or well-foundedness property as assumed data,
  followed by a tautological projection.
- A definition or executable comparison example presented as the missing proposition.
- The repository label `已验证` as human-proof or machine-proof evidence.

No canonical Lean target is frozen at intake because the source record does not identify one.
