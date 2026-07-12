# THM-M-0336 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "Connes
classification theorem". The source inventory supplies only the gloss "classification of
injective von Neumann algebras", Alain Connes, and the year 1976. It does not state a proposition.

Those coordinates strongly suggest Connes' 1976 work on injective factors, but they do not decide
whether the target is a single uniqueness theorem, the paper's package for cases `II_1`,
`II_infinity`, and `III_lambda` with `lambda != 1`, or a later broader classification commonly
described using amenability, hyperfiniteness, and separable-predual hypotheses. In particular, a
blanket claim that all injective factors are classified would silently absorb later results and
unspecified conventions. Intake therefore freezes the ambiguity rather than inventing a theorem.

The root remains `[H1, M4, R4]`. A pinned Lean probe confirms only that mathlib has abstract and
concrete von Neumann algebra structures, commutants, and star projections. It does not provide or
prove injectivity, amenability, hyperfiniteness, factor types, or Connes' classification. Exact
commands and results are recorded in `validation.md`.
