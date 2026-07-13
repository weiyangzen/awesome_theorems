# THM-M-0216 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`高斯-博内定理` ("Gauss-Bonnet theorem"). The catalog attributes the topic to Carl Gauss and
Pierre Bonnet, gives the year 1848, and supplies only the gloss `曲面全曲率与拓扑的关系`
("the relationship between a surface's total curvature and topology"). It provides no cited
mathematical source, exact formula, definitions, hypotheses, boundary convention, proof, or formal
artifact. Its `已验证` ("verified") label is untrusted metadata under rev-5.6.

The gloss does not select one proposition. It could denote the closed-surface identity
`integral K dA = 2 * pi * chi(M)`, the smooth-boundary formula with geodesic curvature, or the
piecewise-smooth formula with corner angles. It also leaves the meaning of surface, regularity,
compactness, orientability, connectedness, curvature and measure normalization, Euler
characteristic, and exceptional cases open. Choosing the familiar closed formula at intake would
add proposition-changing mathematics not fixed by the repository source.

This intake freezes that ambiguity and its non-substitution boundary while leaving the canonical
mathematical and Lean statements null. The provisional root vector is `[H1, M4, R4]`: `H1` records
the recognizable historically proved theorem family while its exact source, variant, assumptions,
and proof crosswalk remain unaudited; `M4` records that no usable exact formal artifact is admitted;
and `R4` records that no source-faithful proof reconstruction can precede exact statement selection.

`IntakeProbe.lean` checks only pinned Riemannian-manifold and homological Euler-characteristic APIs.
Those interfaces do not supply Gaussian curvature, geodesic curvature, surface integration, a
topological Euler characteristic of the same surface, or their Gauss-Bonnet bridge. All six
downstream phases remain open. No canonical statement, H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.

The structured scope authority is `instance.json`, the open workflow authority is `task-dag.json`,
and `intake-receipt.json` is an unsigned provisional worker receipt. The two scope/crosswalk files
record the mathematical boundary, `validation.md` records exact checks and limitations, and
`check_intake.py` rechecks their agreement. None is accepted validation authority until the
integration lane independently accepts a content-addressed receipt.
