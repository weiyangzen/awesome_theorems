# THM-M-0047 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the LU
decomposition theorem. The repository says only that a matrix can be written as a product of a
lower-triangular matrix and an upper-triangular matrix, attributes the result to Alan Turing in
1948, and labels it verified. Under rev-5.6 that label is untrusted inventory metadata, not a
source-reviewed proposition or machine-proof evidence.

Read universally and without pivoting or hypotheses, the gloss is false. Over the rationals, the
matrix `[[0, 1], [1, 0]]` is not `L * U` for lower-triangular `L` and upper-triangular `U`.
`IntakeProbe.lean` kernel-checks this counterexample using mathlib's triangular predicates. A
correct nearby theorem could add a row permutation or impose nonzero-pivot conditions, but either
change alters the proposition and cannot be supplied silently at intake.

The King's College, Cambridge Turing Digital Archive copy of A. M. Turing's "Rounding-off Errors in
Matrix Processes" was inspected. Section 3, journal page 289, proves the precise LDU theorem: if
the principal minors of `A` are nonsingular, unique unit lower-triangular `L`, nonsingular diagonal
`D`, and unit upper-triangular `U` exist with `A = L D U`; the proof continues onto page 290.
Folding `D` into the upper factor explains the catalog family, but deleting its material principal-
minor hypothesis makes the gloss false. Exact terminology/domain mapping, errata, transport, and
independent review remain open, so this source lead is `H1`, not `H0`.

For comparison, van de Geijn and Myers's inspected online *Advanced Linear Algebra: Foundations to
Frontiers*, Theorem 5.2.3.4, gives a precise modern unpivoted variant for full-column-rank complex
matrices: unique LU exists exactly when every principal leading submatrix is nonsingular. Section
5.3.3 instead defines partial-pivoting LU by `P A = L U`. These incompatible valid variants expose
the missing catalog choice; neither is silently adopted as this target.

The provisional vector is `[H1, M4, R4]`. `H1` records that a complete primary proof is known while
the catalog omitted a material source hypothesis and exact mapping remains open. No exact formal
artifact for a corrected root is credited, and no source-faithful reconstruction exists.
`instance.json` freezes this boundary and `task-dag.json` keeps all six downstream phases open. No
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
