# THM-M-1555 rev-5.6 intake

This directory is the fail-closed `planned` intake for the Darboux transformation of a
one-dimensional Schrodinger equation. The repository record fixes only Gaston Darboux, the year
1882, and the phrase "transformation of the Schrodinger equation". It does not identify an exact
source statement or its analytic hypotheses.

The intended theorem family is the first-order intertwining construction obtained from a
nonvanishing seed solution: it changes the potential and maps solutions of the original
second-order spectral equation to solutions of the transformed equation. The sign convention,
regularity, interval, scalar field, spectral parameters, treatment of zeros, and exact source
result remain open for the statement phase. The provisional root vector is `[H3, M4, R4]`; no
exact Lean target, source fidelity, proof, audit completion, or theorem completion is claimed.

`scope-map.md` records the proposition-changing choices, `source-statement-crosswalk.md` separates
repository metadata from source evidence, and `task-dag.json` leaves all downstream work open.
The narrow intake checks and their limits are recorded in `validation.md`.
