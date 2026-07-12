# THM-M-0803 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "inner model
theory". The source inventory gives only the phrase "an inner model of the constructible universe",
attributes it to Ronald Jensen, and dates it to the 1970s. That phrase names a subject or object,
not a proposition: it supplies no ambient theory, definition of inner model, hypotheses, or
conclusion.

Several materially different results lie nearby: the assertion that the constructible universe
`L` is an inner model of ZF/ZFC, Jensen's fine-structure results for `L`, and covering results
relating `L` to the ambient universe. Choosing one would silently substitute mathematics for the
source record. The intake therefore freezes this ambiguity rather than claiming an exact theorem.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib provides a type-level
model of ZFC sets, classes, membership, transitivity, ordinals, and rank. It does not encode a
canonical target for this record, and the probe earns no proof credit. Exact commands and results
are recorded in `validation.md`.
