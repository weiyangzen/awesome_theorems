# THM-M-0266: Stone-Weierstrass theorem

This directory is the rev-5.6 `planned` intake for `S56-M-0266-INTAKE`. The repository catalog
supplies only the name, Marshall Stone, 1937, and the gloss "density of algebras of continuous
functions." That does not identify one exact proposition.

The intake freezes the ambiguity instead of resolving it by convention. In particular, the source
record does not choose the real subalgebra theorem or the RCLike star-subalgebra theorem; a compact
ambient space or compact-set approximation; closure equality, elementwise closure membership, or
an epsilon conclusion; nor the required scalar, topology, separation, and boundary assumptions.

Pinned mathlib contains direct exact-topic interfaces in
`Mathlib.Topology.ContinuousMap.StoneWeierstrass`. `IntakeProbe.lean` checks six of them and reports
the representative axioms, but this is discovery-only interface evidence. No candidate is treated
as the canonical statement or as proof of the catalog claim.

The provisional root vector is `[H1, M3, R4]`. `instance.json` is the intake authority,
`task-dag.json` keeps all six dependent phases open, `scope-map.md` records proposition-changing
choices, and `source-statement-crosswalk.md` records the source boundary. `validation.md` gives the
exact self-test commands. There is no accepted proof state, accepted receipt, audit completion,
theorem completion, or master acceptance.
