# THM-M-0510 rev-5.6 intake

This directory is the fail-closed `planned` dossier for the Hardy-Ramanujan asymptotic formula for
the ordinary integer partition function. The conventional mathematical target is

`p(n) ~ exp(pi * sqrt(2*n/3)) / (4*n*sqrt(3))` as `n -> infinity`,

where `p(n)` counts unordered partitions of the nonnegative integer `n` into positive integers.
This wording fixes the intended scope, but it is not yet an accepted exact-source or Lean statement:
the repository supplies only a one-line gloss, and the original paper's formula/page and assumptions
have not been independently inspected in this phase.

The root remains `[H2, M3, R4]`. A pinned Lean API probe confirms that mathlib provides ordinary
natural-number partitions, their finite cardinality, real asymptotic equivalence, and the real
analytic operations needed to state the conventional formula. It neither proves the formula nor
claims that the probe expression is the canonical target. Exact commands and results are recorded
in `validation.md`.
