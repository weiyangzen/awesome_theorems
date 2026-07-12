# THM-M-1444 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-1444`, the Banach
fixed-point theorem. The repository supplies only the title, Stefan Banach, the year 1922, and the
gloss `压缩映射的不动点` (a fixed point of a contraction mapping). Its `已验证` field is untrusted
catalog metadata, not source or kernel evidence.

The historical source lead was inspected in a publisher-hosted scan bearing the Polish Virtual
Mathematics Library watermark: Stefan Banach, *Sur les opérations dans les ensembles
abstraits et leur application aux équations intégrales*, *Fundamenta Mathematicae* 3 (1922),
133-181, DOI `10.4064/fm-3-1-133-181`. Theorem 6 on printed pages 160-161 states a fixed-point
existence result for a self-operation satisfying a norm contraction with `0 < M < 1`; its proof
iterates from an arbitrary starting element. This is valuable source evidence, but it does not by
itself authorize silently replacing the catalog gloss by a modern complete-metric theorem that
also asserts uniqueness, convergence, or error estimates. The source's earlier axioms for `E`,
incorporated definitions, translation, errata, and independent review remain open.

Pinned mathlib contains several adjacent, materially different contraction APIs. `IntakeProbe.lean`
elaborates them for discovery only. They range from an `EMetricSpace` theorem with a starting point,
finite extended distance, convergence, and a geometric estimate, through a complete-subset variant,
to the standard nonempty complete `MetricSpace` fixed-point, uniqueness, convergence, and estimate
interfaces. No one of these is selected as the canonical target during intake.

The provisional root vector is `[H1, M4, R4]`. `H1` records an identified and inspected published
source theorem whose exact source-to-target incorporation is not yet accepted. `M4` and `R4` record
that there is no source-selected exact Lean target or anchored reconstruction. `instance.json` is
the structured scope authority; the scope map and source-statement crosswalk preserve the open
choices; all six downstream phases remain open in `task-dag.json`. No exact statement, proof,
accepted receipt, audit completion, theorem completion, or master acceptance is claimed.
