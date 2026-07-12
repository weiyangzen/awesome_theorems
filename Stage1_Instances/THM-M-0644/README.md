# THM-M-0644 rev-5.6 intake

This directory is the `planned` intake dossier for the first-order compactness theorem. The
repository statement is specific enough to freeze the human claim: a first-order theory has a
model if and only if each finite subtheory has a model. Here "model" means a nonempty structure
satisfying the theory; "finite subset" means a finite set of sentences contained in that theory.

The pinned mathlib snapshot contains an exact-looking formal candidate,
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable`. `IntakeProbe.lean` checks its
name, type, and the two definitions used by the repository wording. This is discovery evidence for
the next phase, not an accepted statement fingerprint or proof receipt. The primary historical
source, its exact theorem/page, assumptions, and errata also remain to be audited.

The lifecycle remains `planned` at `[H1, M4, R4]`. There is no accepted proof state, audit
completion, or theorem completion. The scope map, source crosswalk, and open task DAG record the
precise downstream boundary; `validation.md` records this intake's self-tests.
