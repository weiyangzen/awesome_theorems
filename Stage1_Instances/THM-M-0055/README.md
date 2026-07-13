# THM-M-0055 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0055`, the repository label
`瑞利商定理` (Rayleigh quotient theorem). The catalog attributes the item to John William Strutt
(Rayleigh), gives the year 1870, and supplies only the gloss `Hermite矩阵特征值的变分刻画`
(variational characterization of Hermite/Hermitian-matrix eigenvalues), plus an explicitly
untrusted `已验证` status. It gives no formula, citation, scalar field, matrix size, eigenvalue
ordering, extremum orientation, attainment clause, or boundary convention.

The word `Hermite` is preserved literally. It is plausibly intended to mean Hermitian, but intake
does not silently repair source text. A modern complete proof lead for real symmetric matrices was
inspected: Daniel A. Spielman's 2025 draft *Spectral and Algebraic Graph Theory*, Chapter 2,
Theorems 2.0.1 and 2.2.1. It defines the Rayleigh quotient, identifies the largest and smallest
eigenvalues with its maximum and minimum, gives selected extremizing eigenvectors, proves that a
maximizer is a top-eigenvalue eigenvector, and states the corresponding minimum direction. It also
states the full indexed Courant-Fischer theorem, which is an explicit non-substitute owned by the
neighboring `THM-M-1390` unless a reviewed source boundary says otherwise. The catalog neither
cites this source nor freezes the exact extremal conclusion, and the source's real-symmetric domain
is narrower than a complex Hermitian reading. It is therefore a source lead, not an admitted root.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M3, R4]`: the theorem family and a complete proof source for one plausible real-symmetric
extremal/Courant-Fischer family are known; exact source and
variant selection, premise and proof-boundary mapping, corrections, and independent review remain
open; pinned mathlib exposes close Rayleigh-quotient, extremal-eigenvalue, Hermitian-matrix, and
sorted-spectrum interfaces, but no source-approved exact target has been frozen; and there is no
reviewed readable reconstruction of that target.

`IntakeProbe.lean` elaborates only those adjacent pinned interfaces. It declares no target and gives
no statement or proof credit. All six downstream phases remain open in `task-dag.json`. No
canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
