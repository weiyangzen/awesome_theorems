# THM-M-1335 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`解的延拓定理` (solution continuation theorem). The repository supplies only the gloss
`解的最大存在区间` (the maximal interval of existence of a solution), the attribution
"many mathematicians," and the twentieth century. Those data identify an ordinary-differential-
equation continuation family, but they do not determine one truth-valued proposition.

The gloss can refer to existence and uniqueness of a maximal solution, an endpoint extension
criterion, escape from compact subsets at a finite maximal endpoint, a norm blow-up alternative,
or a global-existence corollary. These statements require different domains, regularity and
uniqueness hypotheses, solution encodings, and endpoint conventions. This intake preserves the
family boundary rather than selecting a convenient variant from memory.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 2.6, is an
inspected authoritative discovery source. It separates the unique maximal-solution theorem from
the extension, compact-continuation, compact-escape, and whole-space blow-up results. The
repository does not cite that source or select any one of those results, so it is not accepted as
the canonical source at intake.

The provisional root vector is `[H5, M4, R4]`. Here `H5` classifies the supplied catalog wording as
not yet a stable proposition; it does not say that the standard continuation theorems are false or
open. Pinned mathlib provides local integral-curve, Picard-Lindelof existence, and ODE uniqueness
interfaces, but the bounded intake search found no maximal-solution or continuation declaration.

The structured scope authority is `instance.json`. `scope-map.md` records proposition-changing
choices and prohibited substitutions, while `source-statement-crosswalk.md` maps the catalog and
inspected source family to the decisions still required. All six downstream phases remain open in
`task-dag.json`. `IntakeProbe.lean` checks adjacent pinned APIs only and states no target theorem.
No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
