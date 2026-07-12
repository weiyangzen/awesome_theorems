# THM-M-0311 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Riesz-Fischer theorem. The
repository narrows that name to "completeness of L^2 spaces", but it does not specify the measure
space, real versus complex scalars, the quotient by almost-everywhere equality, or a pinpoint
source statement. It also does not say whether the historical Fourier-series formulation is meant
as the root or only as a consequence of abstract L^2 completeness.

The intended scope is therefore recorded without selecting a canonical Lean expression. A bounded
probe confirms that pinned mathlib exposes `MeasureTheory.Lp` and synthesizes its completeness
instance at exponent `2` for real- and complex-valued functions over an arbitrary measure. That is
encoding and candidate-anchor evidence only; statement identity and proof provenance belong to
later phases.

The root remains `[H1, M4, R4]`. No primary-source review, exact statement, accepted proof state,
audit completion, or theorem completion is claimed. `validation.md` records the exact intake checks.
