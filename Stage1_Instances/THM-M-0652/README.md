# THM-M-0652 rev-5.6 intake

This is the `planned` dossier for Craig's first-order interpolation theorem. The terse repository
source says only "existence of an interpolating formula"; this intake resolves that ambiguity to
the classical semantic, sentence-level, first-order theorem while recording the unresolved source
and encoding checks rather than inheriting the legacy `已验证` label.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | semantic entailment between first-order sentences implies existence of a common-language interpolant | Exact elaboration and normalized expression fingerprint belong to the statement phase |
| Languages | one ambient first-order language; the interpolant's symbols must occur in both endpoint sentences | Four-language encodings require a later checked transport and exact-intersection premise |
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

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. At intake time the first failed
theorem gate was the exact Lean statement gate. The statement-phase artifacts below now propose
an elaborated target and evidence, but acceptance, proof, and all later gates remain open. The
theorem is not complete.

## Provisional statement-phase result

`Statement.lean` now elaborates the exact classical semantic, sentence-level target in one ambient
language. Unlike the historical four-language candidate, it enforces the full common-vocabulary
condition: a symbol of the interpolant must occur in each endpoint sentence. The transparent
`statement_iff` transport, empty-language boundary probe, package projection, and three guarded
mutations elaborate with the pinned Lean/mathlib environment. Exact hashes and commands are in
`statement.json` and `statement_validation.md`. This result is provisional until master acceptance
and supplies no proof or theorem-completion credit.

## Validation

Commands and exact results for base revision `9c650bd6aac0dca129c8bc8ac01e0d7432669386`
are recorded in `validation.md`. They establish target membership, standard consistency, JSON
syntax, scoped references, and whitespace hygiene only.
