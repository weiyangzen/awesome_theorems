# THM-M-0890 rev-5.6 dossier

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

The statement phase selects exactly Haemers' Theorem 1 regular unweighted independence-number
ratio bound. `Statement.lean` freezes it for finite nonempty simple graphs of positive regular
degree, with the least eigenvalue obtained from mathlib's descending Hermitian eigenvalue
enumeration. The positive-degree premise makes the source's implicit nonzero-denominator boundary
explicit; equality, weighted, arbitrary-graph, Laplacian, clique, and chromatic variants remain
excluded. `statement.json` and `statement-validation.md` record the full selection and validation
boundary.

`IntakeProbe.lean` remains historical discovery-only intake evidence. The statement worker adds no
proof of Hoffman's bound: it proposes `[H1, M3, R4]`, with H0 source genealogy, anchor audit,
obligation freeze, proof, trust, readability, validation, release, audit completion, theorem
completion, and master acceptance still open. The intake and statement worker states are
provisional evidence only; the master execution authorities are not edited here.
