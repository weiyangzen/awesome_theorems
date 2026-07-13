# THM-M-0891 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Herbert Wilf's 1967 graph-spectrum
theorem. The repository gives only the gloss `色数的谱下界`, literally "a spectral lower bound for
the chromatic number", plus an untrusted `已验证` label. It supplies no formula, graph conventions,
hypotheses, citation, proof boundary, or formal artifact.

The matching primary bibliographic record is H. S. Wilf, *The Eigenvalues of a Graph and Its
Chromatic Number*, Journal of the London Mathematical Society s1-42 (1967), pages 330-332, DOI
`10.1112/jlms/s1-42.1.330`. Publisher and scholarly metadata identify this paper, but the closed
primary text was not lawfully available for statement inspection during intake.

A versioned modern source attributes to Wilf the familiar inequality
`chi(G) <= 1 + lambda_1(G)`, where `lambda_1` is the largest adjacency eigenvalue, and says equality
holds exactly for complete graphs and odd cycles. This is an upper bound on the chromatic number,
or equivalently a lower bound `lambda_1(G) >= chi(G) - 1` on the spectral radius. The catalog's
wording therefore does not determine which orientation or object is intended, whether the equality
classification belongs to the target, or whether connectedness is a root assumption.

`IntakeProbe.lean` authenticates only adjacent pinned mathlib coloring, adjacency-matrix, Hermitian
spectrum, and connectedness interfaces. It declares no theorem and gives no Wilf proof credit. A
bounded repository and pinned-mathlib search found no exact Wilf spectral-coloring declaration.

The provisional vector is `[H1, M4, R4]`: a credible primary bibliographic match and secondary
statement lead exist, but no primary statement is admitted or independently reviewed; no exact
formal artifact is credited; and no source-faithful readable reconstruction can attach to an
unfrozen root. All six dependent phases remain open. No accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
