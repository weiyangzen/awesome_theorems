# THM-M-0511 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Rademacher exact formula for the
integer partition function. The repository source says only "an exact formula for the integer
partition function" and names Hans Rademacher and 1937. It does not specify the summand, the
Dedekind-sum/root-of-unity convention, the domain of `n`, or a theorem/page in a primary source.

The intended historical theorem is the convergent Rademacher series for `p(n)`, not the earlier
Hardy-Ramanujan asymptotic formula. This intake records the standard displayed formula only as a
candidate transcription. Exact source inspection must freeze all signs, normalizations, binders,
and boundary cases before a canonical Lean proposition is created.

The root remains `[H1, M3, R4]`. A pinned Lean probe confirms that mathlib provides the finite type
`Nat.Partition n`, complex exponentials, real derivatives, and infinite-sum predicates needed for a
future encoding. It is an API probe, not the Rademacher statement or a proof. Exact commands and
results are recorded in `validation.md`.
