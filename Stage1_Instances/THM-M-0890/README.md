# THM-M-0890 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0890`, the repository label
`Hoffman bound`. The catalog attributes it to Alan Hoffman in 1970 and supplies only the gloss
`spectral upper bound for independent sets`. It gives no citation, quantified proposition, graph
model, regularity assumption, eigenvalue convention, coefficient field, denominator conditions,
or equality clause. Its `verified` field is untrusted metadata under rev-5.6.

A precise modern source lead is Willem H. Haemers, *Hoffman's ratio bound*, Linear Algebra and its
Applications 617 (2021), 215-219, DOI `10.1016/j.laa.2021.02.010`, arXiv `2102.05529v2`.
Theorem 1 states the familiar regular-graph bound
`alpha <= n * (-lambda_min) / (k - lambda_min)`. The same article explains that Hoffman did not
publish this independence-number result and warns that Hoffman's 1970 coloring paper is often
cited incorrectly for it. That directly conflicts with treating the catalog's author/year fields
as a pinpoint primary proof citation.

The catalog wording still does not select whether the target is the regular unweighted ratio
bound, an arbitrary-graph or weighted extension, an equality characterization, or a bound for one
independent set rather than the independence number. `instance.json` therefore freezes the
provisional vector `[H1, M4, R4]` and leaves the canonical mathematical and Lean statements null.

`IntakeProbe.lean` elaborates only adjacent pinned APIs for finite simple graphs, independent sets,
regularity, adjacency matrices, Hermitian eigenvalues, and positive semidefinite matrices. The
probe neither states nor proves a Hoffman bound. All six downstream tasks remain open in
`task-dag.json`. No H0, M0, R0, accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
