# THM-M-0342 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Plancherel's theorem. The repository
claim is that the Fourier transform is an isometry on `L^2`. The intended scope is the normalized
Fourier transform on complex-valued square-integrable functions over finite-dimensional real
Euclidean space, with equality of `L^2` norms (and the corresponding inner-product preservation).

The statement phase freezes the repository-scope claim as
`Stage1Instances.THM_M_0342.PlancherelTarget`: for every finite dimension, mathlib's normalized
Fourier transform preserves the norm of every complex `L2` class on the corresponding real
Euclidean space. The exact expression, environment fingerprint, and four structural mutations are
recorded in `statement.json` and `statement-validation.md`.

The source record still lacks an inspected primary-source passage and therefore receives no `H0`
credit. Inner-product preservation, inversion, and surjectivity are not credited alternate targets.
No accepted proof state, audit completion, or theorem completion is claimed.

The provisional root is `[H1, M2, R4]`, pending master acceptance of the statement node. Intake
commands are in `validation.md`; statement commands are in `statement-validation.md`.
