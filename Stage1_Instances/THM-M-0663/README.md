# THM-M-0663 rev-5.6 statement dossier

This directory is the fail-closed `planned` intake dossier for the repository label "o-minimal
structures". The only repository statement is "properties of o-minimal structures". That wording
does not identify a unique theorem: o-minimality is a definition, while monotonicity, definable
choice, dimension results, and cell decomposition are distinct theorems with different hypotheses.

The intake-selected root family is the one-variable monotonicity theorem for definable functions in
an o-minimal expansion of a dense linear order. `Statement.lean` now freezes and elaborates that
exact formal target, including the compatible ordered structure, parameter-definable domain and
restricted graph, finite pairwise-disjoint order-convex partition, and continuity/constant/strictly
monotone alternatives. It does not absorb the separate cell-decomposition target `THM-M-0664`.

The target elaborates with three minimal pinned imports. Its checked definitional expansion, four
structural mutations, and empty-domain boundary proof provide statement evidence only. The bounded
anchor audit checks pinned mathlib and three external Lean repositories at immutable revisions; it
finds useful interfaces and partial developments, but no exact terminal proof body. The exact
primary-source theorem/page, proof, and all downstream gates remain open. The lifecycle remains
`planned`; there is no accepted proof state, audit completion, or theorem completion.
