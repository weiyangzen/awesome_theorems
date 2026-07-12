# THM-M-1390 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1390`, the repository label
`Courant极小极大原理` (Courant min-max principle). The catalog supplies Richard Courant, 1920,
and only the gloss `特征值的变分刻画` (variational characterization of eigenvalues), plus an
explicitly untrusted `已验证` status. It gives no formula, source locator, operator, function space,
boundary condition, spectral assumptions, ordering convention, or conclusion.

Courant's 1920 paper *Ueber die Eigenwerte bei den Differentialgleichungen der mathematischen
Physik* was inspected as the strong historical source lead. Its Section 3, Satz 3a on journal pages
18-19 gives a maximum-minimum characterization of the nth eigenvalue for a weighted self-adjoint
elliptic boundary-value problem. That result is materially more specific than the catalog gloss.
The catalog does not cite Satz 3a or determine whether it instead intends a finite-dimensional
Courant-Fischer formula, a compact self-adjoint operator theorem, or a modern quadratic-form
version. Intake therefore records the source lead without silently adopting any variant.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H1, M4, R4]`: an established theorem family and a primary source lead are known, but exact result
selection, premise mapping, translation/correction review, and independent review remain open; no
usable exact formal artifact or source-faithful reconstruction is identified.

`IntakeProbe.lean` elaborates only adjacent pinned Rayleigh-quotient and finite-dimensional spectral
interfaces. The extremal-eigenvalue results it checks are not a kth-eigenvalue min-max theorem and
receive no statement or proof credit. All six downstream phases remain open in `task-dag.json`.
No canonical statement, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
