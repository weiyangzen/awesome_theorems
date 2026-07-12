# THM-M-0567 rev-5.6 intake

This directory is the `planned` intake for Chern characteristic classes. The repository source says
only "characteristic classes of complex vector bundles." That phrase names a family of invariants,
not one proposition with fixed binders and a conclusion. In particular, it does not choose between
existence, axiomatic uniqueness, pullback naturality, the Whitney sum formula, normalization on
line bundles, rank vanishing, or a Chern-Weil comparison theorem.

The provisional root vector is `[H4, M4, R4]`. The scope map records the mathematical subject and
the choices needed to obtain an exact statement. The source crosswalk records only what the local
source supports and deliberately gives no proof credit to the untrusted `已验证` label. No Lean
theorem, proof state, audit completion, or theorem completion is claimed.

## Intake boundary

The dependent statement phase must select an exact source theorem before choosing a Lean encoding.
It must fix the category of complex vector bundles, base-space hypotheses, coefficient ring and
cohomology theory, grading and rank conventions, ordered binders, all conclusions, and boundary
cases. Selecting a convenient isolated identity would substitute for the unresolved source target.

Exact commands and results for this intake are recorded in `validation.md`. Master acceptance is
still required.
