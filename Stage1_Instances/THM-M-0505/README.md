# THM-M-0505 rev-5.6 intake

This directory is the `planned` rev-5.6 intake dossier for the repository label
"Weil explicit formula". The repository source attributes it to Andre Weil,
dates it to 1952, and supplies only the gloss "an explicit formula for the zeta
function".

That gloss identifies a theorem family, not one exact identity. Weil-style
explicit formulae relate a sum over nontrivial zeta zeros to prime-power terms,
archimedean terms, and transforms of an admissible test function. Different
sources use materially different test-function spaces, Fourier/Mellin
normalizations, zero multiplicities, and placements of pole and trivial-zero
terms. The intake therefore freezes this family and its exclusions without
inventing an exact equation.

The scope map and source-statement crosswalk record the decisions required by
the dependent statement phase. `IntakeProbe.lean` checks only that the pinned
Lean environment exposes relevant zeta, von Mangoldt, Fourier, integral, and
Gamma APIs. It states and proves no explicit formula.

Lifecycle is `planned`; the provisional root vector is `[H2, M4, R3]`. There is
no accepted proof state, exact Lean target, audit completion, or theorem
completion. Exact commands and results are recorded in `validation.md`.
