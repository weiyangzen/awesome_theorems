# THM-M-0687 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "ordinal
analysis". The source inventory supplies only the gloss "ordinal measure of proof strength",
attributes the topic to Gerhard Gentzen, and gives 1936. It does not identify a formal theory, an
ordinal notation system, a definition of proof-theoretic ordinal, or a proposition.

Ordinal analysis is a research method and program, not one theorem. Plausible targets include a
consistency result for Peano arithmetic using induction below epsilon zero, a calibration statement
identifying the proof-theoretic ordinal of a named theory, or a general definition relating theories
to ordinals. These are not interchangeable. Selecting one from the metadata alone would substitute
new mathematics for the repository record.

The intake therefore freezes the ambiguity and exclusion boundary rather than inventing a theorem.
The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib provides ordinals,
well-founded ordinal order, epsilon zero, and ordinal notations below epsilon zero; these are only
candidate encoding ingredients. Exact commands and results are in `validation.md`.
