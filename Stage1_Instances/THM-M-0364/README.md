# THM-M-0364 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label "T1 theorem".
The inventory identifies David and Journe's 1984 result and gives only the gloss "L2 boundedness
of singular integral operators". That gloss is a conclusion, not a theorem statement: it omits the
operator/kernel class, weak boundedness condition, the meanings of `T(1)` and `T*(1)`, the BMO
space, and the precise equivalence or implication asserted.

The bibliographic identity is corroborated by the Annals record for Guy David and Jean-Lin
Journe, *A boundedness criterion for generalized Calderon-Zygmund operators*, Annals of
Mathematics 120 (1984), 371-397, DOI `10.2307/2006946`. The article itself and its theorem text
were not available in the repository and were not accepted as a statement source during this
intake. A later statement phase must inspect an immutable copy and freeze the exact theorem.

The root remains `[H1, M4, R4]`. A pinned Lean probe confirms only that mathlib's measure, `MemLp`,
and continuous-linear-map APIs needed by a future encoding are available. It is not a canonical
statement or proof. Exact commands and results are recorded in `validation.md`.
