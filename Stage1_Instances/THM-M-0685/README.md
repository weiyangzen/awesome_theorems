# THM-M-0685 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Gentzen's consistency proof. The
repository supplies the claim `PA` is consistent, Gentzen, and 1936, but it does not specify a
formal presentation of Peano arithmetic, a proof calculus, the consistency predicate, the ordinal
notation system below epsilon-zero, or the metatheory in which transfinite induction is available.
Those choices are part of the theorem, not implementation details.

The scope map therefore records the historically intended theorem family without choosing a
broader semantic satisfiability result or assuming consistency as data. The likely root is a
syntactic result that no derivation of contradiction exists in a fixed calculus for first-order
PA, proved by ordinal reduction justified by a precisely bounded transfinite-induction principle.
Its exact source-faithful formulation remains blocked on primary-source and modern-presentation
pinpointing.

Pinned mathlib exposes first-order theories, semantic satisfiability, ordinals, and epsilon-zero.
`IntakeProbe.lean` checks only these nearby APIs. They neither define PA's derivability relation nor
formalize Gentzen's reduction proof, and receive no proof credit.

The lifecycle is `planned` at `[H1, M4, R4]`. Exact statement identity, source acceptance, Lean
elaboration and mutations, obligation freezing, proof, and release evidence remain open. The
repository's untrusted `已验证` label is not evidence, and no theorem completion is claimed.
