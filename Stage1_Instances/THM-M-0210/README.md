# THM-M-0210 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `笛沙格定理`
(Desargues's theorem). The catalog attributes it to Girard Desargues in 1648, supplies only the
gloss `两个三角形透视的条件` ("the condition for two triangles to be in perspective"), and labels
it `已验证`. That label is untrusted metadata, not a source audit, an exact Lean proposition, or
proof evidence.

The gloss identifies the classical Desargues theorem family but does not determine one proposition.
It does not say whether the intended implication is perspective from a point to perspective from a
line, the converse, or both. It also leaves open affine versus projective incidence, intersections
at infinity, the ambient dimension and coordinate assumptions, the meaning of corresponding sides,
and all nondegeneracy conditions. Intake does not silently select a familiar version.

Two authoritative modern leads were inspected. Magaud, Narboux, and Schreck state the conventional
projective point-to-line implication and formally analyze it in Coq, including its independence from
bare projective-plane axioms and a rank proof in dimension at least three. Hilbert's Section 22,
Theorem 32 states an affine parallel-side specialization and its converse. Together they confirm
that direction, ambient axioms, dimension, degeneracy, and infinity handling are substantive
choices. Neither source is cited by the catalog or independently accepted here, so both support
discovery only, not `H0`, Lean proof credit, or a canonical statement.

Pinned mathlib supplies affine collinearity, affine spans, projectivization, projective subspaces,
and three-dimensional cross-product interfaces. `IntakeProbe.lean` authenticates those APIs. A
bounded exact-topic search found no Desargues declaration or complete perspective-triangle
incidence package. The checked APIs are substrate, not a formal candidate for the root.

The provisional root vector is `[H1, M4, R4]`: a recognizable classical theorem and inspected
authoritative human and Coq source leads exist, but exact source fidelity is unreviewed; no usable
exact Lean artifact is credited; and no source-faithful readable proof exists. `instance.json` is
the scope authority, while `task-dag.json` keeps all six downstream phases open. No canonical statement,
H0, M0, R0, accepted execution state, audit completion, theorem completion, or master acceptance
is claimed.
