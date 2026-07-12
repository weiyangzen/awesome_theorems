# THM-M-1424 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry "random
dynamical systems" (`随机动力系统`). The repository supplies only the gloss "dynamics of
stochastic differential equations" (`随机微分方程的动力学`), attributes the entry to Ludwig
Arnold, and gives 1998. That wording names a subject and construction family, not one truth-valued
theorem with ordered binders, hypotheses, and a conclusion. The catalog label `已验证` is untrusted
under rev-5.6 and provides no source or proof credit.

Arnold's 1998 monograph is a strong bibliographic match. Its first chapter defines random
dynamical systems and contains multiple results about cocycles and invariant measures; its second
chapter contains several distinct generation theorems relating random or stochastic differential
equations to random dynamical systems. The catalog does not select among those results. Choosing a
cocycle definition, a global or local generation theorem, a perfection theorem, an invariant-
measure theorem, or another property would invent missing mathematics.

This intake freezes that ambiguity and the proposition-changing choices an approved source
correction must make. The provisional root vector is `[H5, M4, R4]`. Here `H5` means only that the
catalog wording is not yet a stable proposition; it does not refute or declare open the standard
theory. No exact formal artifact or readable proof can be attached to an unidentified proposition.

The structured intake is `instance.json`; `scope-map.md` records the permitted boundary, and
`source-statement-crosswalk.md` records the source evidence. All six dependent phases remain open
in `task-dag.json`. `IntakeProbe.lean` checks adjacent pinned Lean APIs only and states no target
theorem. Exact worker checks are in `validation.md` and the provisional receipt. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
