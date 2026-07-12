# THM-M-0705 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Church-Rosser theorem. The
repository fixes the topic as confluence of lambda calculus, but it does not provide a source
edition, theorem number, formal term syntax, treatment of alpha-equivalence, or a choice among
beta, beta-eta, and other reduction relations.

The intended standard claim is provisionally scoped as confluence of reflexive-transitive beta
reduction on untyped lambda terms: two reductions from one term have a common reduct. That wording
is a scope map, not yet an exact source statement or canonical Lean target. The statement phase must
inspect an immutable source and settle the remaining representation and reduction choices without
silently replacing the theorem by generic abstract confluence.

A narrow pinned Lean probe confirms that mathlib provides generic relation closures, joins, and a
generic sufficient condition named `Relation.church_rosser`. It does not provide lambda-term syntax
or establish confluence for beta reduction, and receives no proof credit. The root remains
`[H1, M3, R4]`; exact commands and results are recorded in `validation.md`.
