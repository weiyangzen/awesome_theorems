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

Accordingly, the historical intake left the canonical mathematical statement and Lean target null,
recorded the root as `[H1, M3, R4]`, and opened the six downstream tasks. The statement phase below
supersedes that null-target snapshot for current dossier replay, without adding accepted proof state,
audit completion, theorem completion, or master acceptance.

## Statement-phase result

The statement phase provisionally resolves the catalog's variant ambiguity by reading "maximum
size" literally. `ErdosKoRadoMaximumTarget` states the standard positive uniform-family maximum:
for `1 <= r <= n / 2`, a star attains `choose (n - 1) (r - 1)`, and every intersecting `r`-uniform
family has at most that cardinality. It neither substitutes the broader original at-most-size
antichain theorem nor silently adds a classification of all equality families.

`Statement.lean` uses only the low-level `Intersecting` and `Slice` modules, not the proof-bearing
Kruskal-Katona module. It checks a concrete-star iff, the positive-uniform bridge between self-pair
and distinct-pair intersection, the small-ground-set and `n = 2r` boundaries, and four structural
mutations. `check_statement.py`, `statement.json`, `statement-validation.md`, and
`statement-receipt.json` bind the exact elaborated expression and pinned environment.

The vector remains `[H1, M3, R4]`. This is a worker-self-tested statement proposal pending
dependency-ordered master acceptance; no universal upper-bound proof body, equality
classification, `H0`, `M0`, `R0`, audit completion, theorem completion, or release is claimed.
