# THM-M-0652 rev-5.6 intake

This is the `planned` dossier for Craig's first-order interpolation theorem. The terse repository
source says only "existence of an interpolating formula"; this intake resolves that ambiguity to
the classical semantic, sentence-level, first-order theorem while recording the unresolved source
and encoding checks rather than inheriting the legacy `已验证` label.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | semantic entailment between first-order sentences implies existence of a common-language interpolant | Exact elaboration and normalized expression fingerprint belong to the statement phase |
| Languages | explicit common, left, right, and joint languages with commuting language maps | Whether the common language is exactly the symbol intersection needs source and support auditing |
| Semantics | empty-theory model-theoretic consequence on both sides | Theory-relative interpolation is excluded from this root |
| Alternate route | proof-calculus derivability plus soundness/completeness | Candidate architecture only; no bridge is credited |
| Boundary cases | empty common language and coincident side languages are included | Mutation and inhabitation probes remain open |
| Foundations | Lean 4 kernel and pinned mathlib first-order model theory | Toolchain, imports, classical/choice/quotient closure, and TCB fingerprints remain open |

The later obligation tree must preserve distinct syntax/language-map, semantic consequence,
soundness/completeness, cut-free derivation, interpolant extraction, support/common-vocabulary, and
terminal left/right implication obligations. The historical module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_298.lean` is useful discovery material but receives
no rev-5.6 statement or proof credit at intake.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first failed theorem gate is
the exact Lean statement gate: the candidate has no accepted elaborated-expression hash,
environment fingerprint, checked vocabulary-intersection equivalence, or mutation suite. This
intake is self-tested as a dossier artifact, but the theorem is not complete.

## Validation

Commands and exact results for base revision `9c650bd6aac0dca129c8bc8ac01e0d7432669386`
are recorded in `validation.md`. They establish target membership, standard consistency, JSON
syntax, scoped references, and whitespace hygiene only.
