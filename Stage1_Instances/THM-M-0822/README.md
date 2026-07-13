# THM-M-0822 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the theorem family cataloged as the
Erdős-Ko-Rado theorem with the gloss "maximum size of an intersecting family." The two identical
catalog rows are duplicate metadata, not independent sources or separate targets.

The original 1961 paper was inspected from the Alfréd Rényi Institute's Erdős archive. Its Theorem
1 gives the sharp upper bound for pairwise-incomparable, pairwise-intersecting families of subsets
of an `m`-element ground set when member sizes are at most `l` and `1 <= l <= m / 2`; the following
remark supplies the fixed-`l` star construction showing best possibility. Uniform fixed-size
families are automatically incomparable. The catalog does not say whether its root
is this at-most-size theorem, the now-standard uniform `l`-set upper bound, attainment of the
maximum, or an equality/extremal-family characterization. No independent source reviewer or errata
disposition is yet recorded.

Pinned mathlib contains `Finset.erdos_ko_rado` in
`Mathlib.Combinatorics.SetFamily.KruskalKatona`. The intake probe checks its exact type and axiom
report. Its checked type states the standard uniform-family upper bound, including `r = 0`, but its
declaration does not assert attainment or characterize equality. This is a credible formal
candidate, not accepted proof credit for the still-unselected catalog claim.

Accordingly, the intake leaves the canonical mathematical statement and Lean target null, records
the root as `[H1, M3, R4]`, and opens the six downstream tasks. No exact statement, accepted proof
state, audit completion, theorem completion, or master acceptance is claimed.
