# THM-M-1532 rev-5.6 intake

This is a `planned` dossier for the Standard Model of particle physics. The repository source gives
only the label "the Standard Model" and calls it a theorem/proposition. That label denotes a theory,
not a truth-valued mathematical statement. Intake therefore preserves the ambiguity rather than
inventing a theorem or substituting a convenient gauge-theory lemma.

## Scope map

| Surface | Candidate in-scope content | Intake boundary |
|---|---|---|
| Physical specification | gauge group `SU(3) x SU(2) x U(1)`, fields, representations, couplings, Higgs sector | A source-faithful convention and parameter boundary are not selected |
| Mathematical object layer | Lie groups/algebras, bundles or connections, representations, invariant polynomial terms | No particular spacetime, regularity, or classical/quantum model is frozen |
| Consequence layer | a separately sourced proposition derived from explicit axioms | No consequence may stand in for the whole theory |
| Empirical layer | observations and fitted constants | Evidence is not Lean kernel proof and remains outside machine closure |
| Lean layer | Lean 4 plus pinned mathlib | Module, declaration, imports, and environment fingerprint remain open |

## Intake verdict

The lifecycle is `planned`, with provisional root vector `[H4, M4, R3]`. The first failed gate is
exact source statement identification: there are no binders, hypotheses, or conclusion to elaborate.
The dependent statement phase must select and cite one precise mathematical proposition, or remain
blocked. This dossier makes no theorem-completion claim.

## Validation

The commands and exact scoped results are recorded in `validation.md`. They validate manifest
membership, repository-standard consistency, JSON syntax, and absence of forbidden proof shortcuts;
they do not validate a Lean statement.
