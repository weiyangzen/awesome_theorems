# THM-M-0583 rev-5.6 statement dossier

This directory is the `planned` intake for the four-dimensional topological Poincare conjecture.
The intended human claim is Freedman's result that every closed topological 4-manifold homotopy
equivalent to the 4-sphere is homeomorphic to the 4-sphere. The smooth analogue is explicitly
excluded: it remains open and must not be substituted for the topological theorem.

The source crosswalk identifies a primary publication anchor but does not claim `H0`: a stable copy,
exact printed wording/page, definitions, assumptions, and errata still require independent review.
The statement phase freezes and elaborates the canonical Lean expression in `Statement.lean` using
the pinned mathlib topological-manifold, sphere, homotopy-equivalence, and homeomorphism encodings.
The statement gate is self-tested and awaits master acceptance. The provisional root vector remains
`[H2, M4, R4]`; statement elaboration supplies no proof, audit completion, or theorem completion.

The open downstream nodes are recorded in `task-dag.json`; intake checks are in `validation.md`,
and exact statement evidence is in `statement-validation.md` and `statement.json`.
