# THM-M-1105 rev-5.6 intake

This directory is the fail-closed `planned` intake for the Wigner semicircle law. The repository
record fixes only the name, Eugene Wigner, the year 1955, and the phrase "eigenvalue distribution
of Wigner matrices". It does not fix a matrix ensemble, normalization, convergence mode, or moment
assumptions.

The intended theorem family is convergence of the empirical spectral measure of normalized real
symmetric Wigner matrices to the semicircle probability measure. The exact primary-source version
and all assumptions remain open for the statement phase; no modern variant is silently attributed
to Wigner's original paper. The provisional root vector is `[H2, M4, R4]`. No exact Lean target,
source-fidelity review, proof state, audit completion, or theorem completion is claimed.

`scope-map.md` records the choices that affect the proposition,
`source-statement-crosswalk.md` separates discovery sources from accepted evidence, and
`task-dag.json` keeps every downstream phase open. Validation evidence is in `validation.md`.
