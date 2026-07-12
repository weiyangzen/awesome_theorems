# THM-M-0318 rev-5.6 intake

This directory is the `planned` intake dossier for the Schauder fixed-point theorem. The intended
human claim is the compact-convex form: a continuous self-map of a nonempty compact convex subset
of a real normed vector space has a fixed point. This is narrower and more precise than the Stage0
phrase "a fixed-point theorem on Banach spaces" and does not silently substitute Banach's
contraction theorem or the finite-dimensional Brouwer theorem.

`Statement.lean` now freezes and elaborates that compact-convex claim as
`Stage1Instances.THM_M_0318.SchauderFixedPointTarget`, with a checked direct expansion, structural
mutations, and empty/singleton boundary checks. The exact expression and environment fingerprint
are recorded in `statement.json`. The primary 1930 paper's exact theorem text, page-level anchor,
terminology, and errata remain uninspected, so this statement evidence does not upgrade source
fidelity to `H0`.

The provisional root vector is `[H2, M3, R4]`. The statement node is self-tested pending master
acceptance. No source fidelity (`H0`), proof, audit completion, or theorem completion is claimed.
