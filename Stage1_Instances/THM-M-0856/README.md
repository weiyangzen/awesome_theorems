# THM-M-0856 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0856`, the repository's
`Tutte定理` (Tutte theorem). The catalog gives William Tutte, 1947, and only the gloss
`完美匹配存在的条件` (a condition for the existence of a perfect matching). Its `已验证`
field is untrusted metadata and supplies no source or proof credit.

## Intake result

The name, date, and gloss strongly identify Tutte's 1-factor theorem for finite graphs: a finite
graph has a perfect matching exactly when deleting every vertex subset `U` leaves at most `|U|`
connected components of odd order. The leading primary-source identity is W. T. Tutte, *The
Factorization of Linear Graphs*, Journal of the London Mathematical Society s1-22(2) (1947),
107-111, DOI `10.1112/jlms/s1-22.2.107`. Crossref and OpenAlex metadata confirm that identity, but
no full primary text, exact theorem locator, incorporated definitions, correction history, or
independent source review is admitted. The source mapping therefore remains `H1`, not `H0`.

## Formal boundary

Pinned mathlib contains a direct proof-bearing candidate in
`Mathlib.Combinatorics.SimpleGraph.Tutte`: `SimpleGraph.tutte` states that a finite simple graph has
a perfect matching if and only if it has no `IsTutteViolator`. The violator predicate unfolds to
strictly more odd connected components after deleting `U` than vertices in `U`. `IntakeProbe.lean`
checks these exact interfaces and records the candidate axiom report. This is unusually strong
intake discovery, but statement identity, minimal-import and mutation gates, terminal-body
provenance, and master acceptance belong to later ordered phases. The candidate is classified
provisionally as `M3`, not credited as `M0-W`.

The provisional vector is `[H1, M3, R4]`. All six downstream tasks remain open. No canonical Lean
statement, accepted proof state, H0, M0, R0, audit completion, theorem completion, accepted receipt,
or master acceptance is claimed.
