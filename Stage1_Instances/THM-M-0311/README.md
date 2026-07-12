# THM-M-0311 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the Riesz-Fischer theorem. The
repository narrows that name to "completeness of L^2 spaces", but it does not specify the measure
space, real versus complex scalars, the quotient by almost-everywhere equality, or a pinpoint
source statement. It also does not say whether the historical Fourier-series formulation is meant
as the root or only as a consequence of abstract L^2 completeness.

The statement phase now freezes that repository gloss as
`Stage1Instances.THM_M_0311.RieszFischerTarget`: for every measurable carrier and measure, both the
real- and complex-valued `MeasureTheory.Lp` quotients at exponent `2` are complete. `Statement.lean`
elaborates this exact proposition with the single minimal pinned import, checks a direct-encoding
transport, distinguishes four structural mutations, and exercises zero/empty/infinite boundaries.
The historical Fourier-series realization remains outside the canonical target unless a later
source audit supplies a checked bridge.

The root remains `[H1, M3, R4]`. This is provisional statement evidence pending master acceptance,
not an accepted proof state. No primary-source review, proof-body credit, audit completion, or
theorem completion is claimed. `statement-validation.md` records the exact statement checks.
