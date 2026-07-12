# THM-M-1340 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item
"differentiability of solutions with respect to parameters." The repository gives only the gloss
"derivative of solutions with respect to parameters," attributes it to many mathematicians in the
20th century, and labels it `已验证`. Under rev-5.6 that label is untrusted metadata, not a source
statement or proof result.

The gloss identifies a classical ODE theorem family but not one proposition. It does not fix the
state and parameter spaces, the time-state-parameter domain, the vector field and its regularity,
the initial condition, a common existence neighborhood, whether the parameter also enters the
initial data, the derivative convention, or whether the conclusion includes the sensitivity
equation. A modern source candidate gives one precise finite-dimensional local formulation, but
the catalogue does not select that source or establish that its full `C^k` result is the intended
root.

This intake freezes the received wording, admissible family, proposition-changing decisions, and
boundaries with adjacent targets. It deliberately leaves the canonical mathematical statement and
Lean target null. The root vector is `[H1, M4, R4]`: a standard published theorem family is
identified but no exact source is accepted; no usable theorem-specific Lean artifact was located;
and no source-faithful proof reconstruction can attach before the proposition is frozen.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record the unresolved choices and sources, while `task-dag.json`
keeps all downstream phases open. `IntakeProbe.lean` checks only adjacent pinned ODE and calculus
interfaces. No exact-statement, H0, M0, R0, audit-completion, theorem-completion, or master-
acceptance credit is claimed.
