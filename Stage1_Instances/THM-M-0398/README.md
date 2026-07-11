# THM-M-0398 statement dossier

This is the rev-5.6 `planned` intake for the Thue-Siegel-Roth theorem. The scoped target is the classical rational-approximation form: an irrational algebraic real cannot have infinitely many rational approximations of exponent strictly greater than two.

The canonical prose claim, scope decisions, and source crosswalk are recorded in `instance.json`, `scope-map.md`, and `source-crosswalk.md`. `Statement.lean` now fixes and elaborates the exact rational-set target, using mathlib's `IsAlgebraic ℚ α`, `Irrational α`, normalized `Rat.den`, real powers, and `Set.Finite`. `statement.md` records the encoding and validation boundary.

Current root debt is `[H1, M3, R4]`: the statement is elaborated, but no proof inhabitant or upstream closure is claimed. No legacy artifact is accepted, no proof state is accepted, and neither audit completion nor theorem completion is claimed.

The authoritative local intake state is `instance.json`; this Markdown file is explanatory only.
