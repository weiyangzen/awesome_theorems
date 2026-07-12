# THM-M-0686 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `超限归纳`
(transfinite induction). The complete source wording is only "transfinite induction in proof theory",
with Gerhard Gentzen and 1936 as metadata. That wording does not identify a proposition: it does not
select an ordinal or notation system, a predicate class, an ambient formal theory, or whether the
claim is an external well-founded induction theorem, an internal induction schema, or the induction
principle used in Gentzen's consistency argument.

The scope map preserves these readings without choosing one. Pinned mathlib contains general
well-founded induction on `Ordinal`, as checked by `IntakeProbe.lean`, and ordinal infrastructure
for epsilon zero. These are discovery anchors only. Substituting unrestricted semantic ordinal
induction for a proof-theoretic induction schema would erase the source's central foundation and
strength questions.

The lifecycle is `planned` at `[H3, M4, R4]`. Selecting and independently reviewing an exact
primary-source proposition is the first downstream blocker. No accepted proof state, statement
fingerprint, obligation registry, audit completion, or theorem completion is claimed.
