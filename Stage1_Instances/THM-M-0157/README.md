# THM-M-0157 rev-5.6 intake

This directory is the fail-closed `planned` intake for the repository label "Gauss map theorem".
The source inventory gives Carl Friedrich Gauss, the year 1827, and only the gloss "properties of
the Gauss map of a surface". That wording does not identify a unique proposition. It may refer to
the differential of the unit-normal map, its relation to the shape operator, the determinant/Jacobian
formula for Gaussian curvature, or a global degree/total-curvature result. These claims have different
hypotheses and conclusions and must not be substituted for one another.

The intended family is the classical Gauss-map theory of a regular oriented surface in Euclidean
three-space. The exact source theorem and the local-versus-global variant remain open for the
statement phase. The provisional root vector is `[H1, M4, R4]`. No exact Lean target, source review,
formal candidate, audit completion, or theorem completion is claimed.

`scope-map.md` records the proposition-changing choices,
`source-statement-crosswalk.md` records the source ambiguity and required mapping, and
`task-dag.json` leaves every downstream phase open. The intake checks are recorded in
`validation.md`.
