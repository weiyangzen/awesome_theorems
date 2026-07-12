# THM-M-0552 rev-5.6 intake

This directory is the `planned` intake for the metadata label "Pontryagin operation". The source
gloss, "stable cohomology operations on integral cohomology", does not identify a theorem and does
not match the usual type of the Pontryagin square, which is a degree-doubling operation with
mod-2 input and mod-4 output. "Pontryagin" may also refer to characteristic classes, duality, or
the Pontryagin product; none may be substituted for the intended operation.

The scope map and source crosswalk freeze this ambiguity rather than inventing binders. The first
downstream gate is selection of a primary-source theorem and an exact operation, coefficient,
degree, domain, hypotheses, and laws. No historical `已验证` label is accepted as evidence. The
provisional root vector is `[H1, M4, R4]`; no exact statement, Lean elaboration, proof, audit
completion, or theorem completion is claimed.

The downstream tasks remain open in `task-dag.json`. Scoped intake checks and their exact results
are recorded in `validation.md`.
