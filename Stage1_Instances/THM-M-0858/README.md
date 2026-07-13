# THM-M-0858 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Rowland Brooks's graph-coloring
theorem. The repository catalog supplies only the gloss `图的色数上界` ("an upper bound for the
chromatic number"), the year 1941, and the untrusted label `已验证`. It gives no formula, citation,
definitions, hypotheses, proof boundary, or formal artifact.

The matching original source has been identified: R. L. Brooks, *On colouring the nodes of a
network*, Proceedings of the Cambridge Philosophical Society 37(2) (1941), pages 194-197, DOI
`10.1017/S030500410002168X`. Its theorem paragraph on printed page 194 says that, for `n > 2`, a
possibly infinite loopless network of pointwise degree at most `n`, with no connected component an
`n`-simplex (a complete graph on `n + 1` nodes), admits a proper coloring with `n` colors.

That printed proposition is the intake candidate, but not yet an accepted canonical statement.
The statement phase must admit and independently review an immutable source edition, decide the
simple-graph/parallel-edge transport, and freeze and mutation-test the exact Lean expression. In
particular, it must not silently substitute the familiar finite connected maximum-degree form with
complete-graph and odd-cycle exceptions: the original theorem expressly permits infinite graphs
and restricts to `n > 2`, so the odd-cycle branch is outside its stated domain.

`IntakeProbe.lean` confirms that a source-shaped envelope and the required pinned mathlib APIs
elaborate. It proves no Brooks theorem. A bounded repository and pinned-mathlib search found no
exact Brooks declaration. The provisional root vector is `[H1, M3, R4]`: a pinpoint primary
statement and proof source is located but not admitted to `H0`; the exact proposition is
representable using pinned interfaces but has no credited proof body; and no reviewed readable
reconstruction exists.

All dependent tasks remain open in `task-dag.json`. No accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
