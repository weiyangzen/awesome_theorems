# THM-M-0196 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `九点圆定理`
(nine-point circle theorem). The catalog supplies the gloss `三角形九点共圆` ("the nine points of
a triangle are concyclic"), the attribution Karl Wilhelm Feuerbach, the year 1822, and an
untrusted `已验证` label. It supplies no citation, definition of the nine points, ordered binders,
hypotheses, or circle/concyclicity encoding.

The conventional theorem family concerns the three side midpoints, the three midpoints between the
vertices and orthocenter, and the three altitude feet of a nondegenerate Euclidean triangle. Intake
preserves that reading as a candidate scope, not as an accepted source-exact proposition. The scope
map records the proposition-changing choices that an immutable source review must resolve.

Pinned mathlib contains the exact-topic module
`Mathlib.Geometry.Euclidean.NinePointCircle`. It defines a nine-point circle and separately proves
membership for the three indexed families above. `IntakeProbe.lean` authenticates those declarations
with the pinned Lean environment. This is unusually strong discovery evidence and a prospective
`M0-W` route, but intake is not the statement, anchor-audit, proof, provenance, trust, or acceptance
phase. No single canonical root, checked source transport, accepted proof state, or machine closure
is claimed.

The provisional intake vector is `[H1, M4, R4]`: the named classical theorem is believed proved,
the exact human source mapping remains open, the discovered formal bodies are not yet eligible for
root credit, and no readable proof reconstruction exists. All six dependent phases remain open in
`task-dag.json`. Exact commands and results appear in `validation.md`.
