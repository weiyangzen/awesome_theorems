# THM-M-0262 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog label `沙利定理`
(`Sullivan theorem`). The repository attributes it to Dennis Sullivan, dates it to 1985, and gives
only the gloss `有理函数动力学的分类` (`classification of rational-function dynamics`). Those
words name an author, year, and subject, but they do not give a truth-valued proposition with
ordered binders, hypotheses, an equivalence relation, classified objects, or a conclusion. The
catalog status `已验证` is untrusted metadata under rev-5.6.

The ambiguity is not repaired by choosing a famous Sullivan result from memory. In particular,
`THM-M-1434` separately owns `Sullivan无游荡域定理`, with the explicit gloss `有理函数的无游荡域`
(`no wandering domains for rational functions`). Replacing this target with that result would
broaden one target's scope and duplicate another target's root.

This intake freezes that boundary and leaves the canonical mathematical and Lean targets null. The
provisional vector is `[H5, M4, R4]`: `H5` classifies the received catalog wording as not yet a
stable proposition; it does not say that a reviewed Sullivan theorem is false or open. No exact
usable formal artifact or source-faithful proof reconstruction can attach to an unidentified root.

`instance.json` is the structured scope authority. `scope-map.md` records the proposition-changing
decisions and forbidden substitutions. `source-statement-crosswalk.md` maps the catalog wording to
source leads and the still-open formal components. `task-dag.json` keeps all six dependent phases
open. `IntakeProbe.lean` checks only adjacent pinned APIs and states no target theorem. No H0, M0,
R0, accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
