# THM-M-0398 statement dossier

This is the rev-5.6 `planned` intake for the Thue-Siegel-Roth theorem. The scoped target is the classical rational-approximation form: an irrational algebraic real cannot have infinitely many rational approximations of exponent strictly greater than two.

The canonical prose claim, scope decisions, and source crosswalk are recorded in `instance.json`, `scope-map.md`, and `source-crosswalk.md`. `Statement.lean` now fixes and elaborates the exact rational-set target, using mathlib's `IsAlgebraic ℚ α`, `Irrational α`, normalized `Rat.den`, real powers, and `Set.Finite`. `statement.md` records the encoding and validation boundary.

`anchor-audit.md` inventories pinned mathlib candidates and a bounded external
Lean 4 search. The checked mathlib hits are supporting approximation, height,
and Siegel-lemma infrastructure or an irrelevant combinatorial Roth theorem;
no terminal Thue-Siegel-Roth candidate was found or credited.

Current root debt is `[H1, M3, R4]`: the statement is elaborated, but no proof inhabitant or upstream closure is claimed. No legacy artifact is accepted, no proof state is accepted, and neither audit completion nor theorem completion is claimed.

The obligation phase freezes 15 semantic obligations in
`obligation-registry.json` and seven separate graph families in
`typed-graphs.json`. `ObligationTree.lean` checks the conditional `C = 1`
specialization while leaving the substantive constant-factor Roth engine open;
`obligation-tree.md` and `obligation-validation.md` state the exact boundary.

The authoritative local intake state is `instance.json`; this Markdown file is explanatory only.
