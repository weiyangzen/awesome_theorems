# THM-M-0714 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the MRDP theorem. The repository
gloss says only that recursively enumerable sets are Diophantine. That identifies the standard
theorem family, but it does not freeze the computability predicate, tuple coding, arity convention,
or the exact polynomial representation needed for an exact Lean proposition.

The intended mathematical scope is the forward MRDP implication: every recursively enumerable
subset of a finite power of the natural numbers has an existential integer-polynomial
representation over natural-number witnesses. The converse and Hilbert's tenth problem are
related consequences, not substitutes for this target.

The root remains `[H3, M4, R4]`. A pinned Lean probe confirms that mathlib supplies `Dioph`,
partial-recursive predicates/functions, and the machine-checked `Dioph.pow_dioph` substrate. The
module itself explicitly leaves completion of Hilbert's tenth problem as TODO, so none of these
anchors is credited as the full MRDP theorem. Exact commands and results are in `validation.md`.
