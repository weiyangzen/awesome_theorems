# THM-M-0540 rev-5.6 intake

This directory is the `planned` intake for singular homology. The Stage0 phrase names a theory or
construction rather than a single theorem, so the dossier freezes the intended mathematical scope
without pretending that an exact terminal proposition has already been supplied.

The intended scope is ordinary, unreduced singular homology: continuous standard simplices in a
topological space generate a chain complex whose differential is the alternating sum of face maps,
and degree-`n` homology is the corresponding cycles modulo boundaries. Coefficients, universes, and
the exact theorem-shaped Lean expression remain decisions for the statement phase.

The pinned mathlib checkout exposes `singularChainComplexFunctor` and `singularHomologyFunctor`.
`IntakeProbe.lean` checks only those discovery anchors; it is not a proof of a canonical target. The
provisional root vector is `[H1, M3, R4]`. No H0 source audit, accepted proof state, audit completion,
or theorem completion is claimed.
