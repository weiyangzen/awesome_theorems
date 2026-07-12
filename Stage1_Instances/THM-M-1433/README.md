# THM-M-1433 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `Brjuno条件`
(`Brjuno condition`). The repository attributes the entry to Alexander Brjuno, dates it to 1971,
and gives only the gloss `Siegel盘的线性化条件` (`a linearization condition for Siegel disks`).
That wording does not determine a truth-valued proposition with ordered binders, hypotheses, and a
conclusion. The catalog status `已验证` is untrusted metadata under rev-5.6.

The gloss can refer to an arithmetic predicate, Brjuno's sufficient linearization theorem for a
one-variable holomorphic germ, later necessity/sufficiency results for a whole class of germs or a
quadratic polynomial, or a quantitative radius estimate. These are not interchangeable. They use
different continued-fraction conventions, map classes, quantifier orders, conjugacy normalizations,
and boundary cases; the neighboring `THM-M-1432` separately names Yoccoz's theorem.

This intake freezes that ambiguity rather than selecting a familiar theorem. The provisional root
vector is `[H5, M4, R4]`: `H5` says that the received catalog wording is not yet a stable
proposition, not that Brjuno's published results are false. No exact Lean target, proof body, or
readable proof reconstruction can attach to an unidentified root.

The structured authority is `instance.json`. `scope-map.md` records the permitted boundary and
prohibited substitutions; `source-statement-crosswalk.md` maps the catalog wording to the source
and Lean decisions still required. All six downstream phases remain open in `task-dag.json`.
`IntakeProbe.lean` checks only adjacent pinned Lean APIs and states no target theorem. No H0, M0,
R0, accepted proof state, audit completion, theorem completion, or master acceptance is claimed.
