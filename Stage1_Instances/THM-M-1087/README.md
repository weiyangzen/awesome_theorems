# THM-M-1087 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Fernique's theorem".
The repository source fixes only the wording "an upper bound for a stationary Gaussian process",
attributes it to Xavier Fernique, and gives 1975. That wording does not determine the indexed
process, parameter space, regularity assumptions, random supremum, or the form and constants of an
upper bound.

Pinned mathlib contains the related Banach-space Gaussian-measure theorem
`ProbabilityTheory.IsGaussian.exists_integrable_exp_sq`. `IntakeProbe.lean` confirms that the
declaration is available in the current pinned environment. This is discovery evidence only:
exponential square-integrability of the norm of a Gaussian random vector is not silently treated as
the repository's unspecified stationary-process bound.

The provisional vector is `[H3, M3, R4]`: a theorem family and a checked formal candidate exist,
but exact source identity, source-to-formal equivalence, and the canonical Lean target remain open.
No proof state, audit completion, or theorem completion is accepted. The scope map, crosswalk, and
open task DAG preserve that boundary; exact intake checks are recorded in `validation.md`.
