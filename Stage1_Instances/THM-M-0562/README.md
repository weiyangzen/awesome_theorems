# THM-M-0562 rev-5.6 intake

This directory is the fail-closed `planned` intake for the Thom isomorphism. The repository source
fixes only the phrase "the Thom isomorphism for vector bundles". The intended theorem family is
the classical cohomological isomorphism induced by cup product with a Thom class, but the source
does not fix the bundle category, coefficient system, orientation convention, or base-space
hypotheses.

The scope map records those proposition-changing choices instead of silently selecting a familiar
variant. The source crosswalk identifies stable primary and modern source candidates without
claiming that their exact theorem locators or conventions have been independently accepted. The
provisional root vector is `[H1, M4, R4]`; no exact Lean target, formal anchor, proof, audit
completion, or theorem completion is claimed.

Every downstream rev-5.6 phase remains open in `task-dag.json`. The exact intake checks and their
limits are recorded in `validation.md`.
