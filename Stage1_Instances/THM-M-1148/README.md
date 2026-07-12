# THM-M-1148 rev-5.6 intake

This directory is the `planned` intake dossier for the Poisson integral formula on a disk. The
repository source phrase is "solution of the Dirichlet problem on a disk". Accordingly, the frozen
human scope is the classical theorem that continuous boundary data on a circle has a Poisson-kernel
integral extension which is harmonic in the disk, continuous on its closure, and equals the data on
the boundary. The formal statement fixes the normalization as mathlib's `Real.circleAverage`
applied to `poissonKernel c w • g`. The exact primary-source edition anchor remains open on the
human-source axis.

The nearby legacy module for `THM-M-1154` contains checked mathlib Poisson-kernel anchors, but is a
different theorem and supplies no statement or proof credit here. This intake claims only lifecycle
`planned`, with provisional root vector `[H2, M3, R4]`. It does not claim a proof, audit completion,
or theorem completion.

`Statement.lean` now elaborates the exact target with the single direct import
`Mathlib.Analysis.Complex.Harmonic.Poisson`. Its statement-only evidence is recorded in
`statement.json` and `statement-validation.md`; no proof or theorem completion is claimed.
