# THM-M-0334 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Murray-von Neumann classification". The source inventory gives only the gloss "classification of
von Neumann algebras", the names Francis Murray and John von Neumann, and the year 1936. It does
not state a proposition.

The label commonly points toward the projection-theoretic classification of factors into types I,
II, and III, with further finite/infinite and type-I dimension refinements. But "classification of
von Neumann algebras" can also mean the central decomposition of a general algebra into factor
types, and it does not specify which refinements or equivalence notion are part of the conclusion.
Choosing one of these claims from the title alone would substitute invented mathematics for the
repository target.

The intake therefore freezes this ambiguity and its exclusions rather than a canonical theorem.
The root remains `[H1, M4, R4]`. A pinned Lean probe confirms that mathlib provides abstract and
concrete von Neumann algebra structures, commutants, and star projections, but this is only an API
availability check. It is neither the classification statement nor proof evidence. Exact commands
and results are recorded in `validation.md`.
