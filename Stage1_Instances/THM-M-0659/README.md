# THM-M-0659 rev-5.6 intake

This directory is the `planned` dossier for the repository label **谢拉赫分类定理**
("Shelah classification theorem"). The only accompanying claim is **超稳定理论的分类**
("classification of superstable theories"). Those phrases name a broad research programme, not
an exact proposition: they do not say what objects are classified, by which invariants, under which
cardinality and set-theoretic hypotheses, or what the conclusion means.

## Intake scope

| Surface | Preserved scope | Boundary at intake |
|---|---|---|
| Human root | A theorem attributed to Saharon Shelah concerning classification of superstable first-order theories | Exact theorem, edition, locator, and wording are unresolved |
| Ambient objects | First-order languages, theories, models, elementary embeddings, types, and stability-theoretic structure are discovery surfaces | Completeness, language cardinality, spectrum cardinal, and universe levels are not fixed |
| Classification result | A source-specific classification claim about superstable theories | No substitution by categoricity, stability, decomposition, the main gap, or a spectrum dichotomy is accepted |
| Lean target | Lean 4 with the repository's pinned mathlib closure | No expression is selected before source identification |
| Foundations | Lean kernel, with classical logic and choice to be audited after the claim is known | Exact imports, axioms, TCB closure, and computation policy remain open |

The metadata attribution (Shelah, 1990) is a discovery hint. The inherited `已验证` label is
untrusted under rev-5.6 and grants neither human-source nor machine-proof credit.

## Intake verdict

Lifecycle is `planned`, with provisional root vector `[H5, M4, R4]`. The first failed downstream
gate is identification and independent review of a pinpoint primary statement. The statement phase
must not proceed by choosing whichever theorem is easiest to encode. It must first establish the
intended result and all incorporated definitions and assumptions, then freeze and mutation-test an
exact Lean expression.

The exact commands and results in `validation.md` validate this intake's membership, structure,
JSON, environment availability, and fail-closed boundaries only. No theorem statement or proof is
claimed, and `theorem_complete` is false.
