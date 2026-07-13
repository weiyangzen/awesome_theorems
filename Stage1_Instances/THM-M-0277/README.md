# THM-M-0277 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the closed graph theorem. The
repository supplies only the Chinese gloss `闭线性算子的连续性` ("continuity of closed linear
operators"), attributes it to Stefan Banach in 1932, and labels it `已验证` ("verified"). Under
rev-5.6 that label is untrusted inventory metadata, not a primary-source audit, an exact Lean
proposition, or proof evidence.

The gloss identifies the classical theorem family but leaves proposition-changing choices open.
It does not say whether the operator is everywhere defined, whether both spaces are Banach spaces,
which scalar field is used, which product topology makes the graph closed, or whether continuity or
boundedness is the conclusion. In particular, a closed partially defined unbounded operator is not
the classical total-domain conclusion and must not be substituted for it.

Pinned mathlib contains the direct candidate `LinearMap.continuous_of_isClosed_graph` in
`Mathlib.Analysis.Normed.Operator.Banach`. It states that a total linear map between complete normed
spaces over a nontrivially normed field is continuous when its graph is closed. The sequential
variant and constructors of continuous linear maps are adjacent interfaces. `IntakeProbe.lean`
authenticates these pinned interfaces and representative axiom reports only; none is silently
declared source-identical to the sparse catalogue root.

No pinpoint primary human source was found in the repository. The provisional vector is
`[H1, M3, R4]`: the classical theorem is known, but exact source assumptions, proof boundary,
errata, and source-to-target review remain open; a direct formal candidate exists, but the canonical
statement and checked transport are not frozen; and no source-faithful readable proof
reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` preserve the unresolved statement boundary, while `task-dag.json`
keeps all six downstream phases open. No H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
