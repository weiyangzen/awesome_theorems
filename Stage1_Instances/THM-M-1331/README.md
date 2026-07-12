# THM-M-1331 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalogue item "existence and
uniqueness theorem." The repository gives the gloss "existence and uniqueness of solutions under
a Lipschitz condition," attributes it to Augustin Cauchy and Charles Emile Picard in 1890, and
labels it `已验证`. Under rev-5.6 that label is untrusted metadata, not source or proof evidence.

The gloss identifies an ODE existence-and-uniqueness family but not one proposition. It does
not specify the time and state domains, autonomous versus time-dependent vector field, the
Lipschitz variable and region, continuity and boundedness assumptions, initial data, interval,
endpoint derivative convention, or the class and domain in which uniqueness holds. The adjacent
catalogue target `THM-M-1332` separately names the Picard-Lindelof theorem, so silently making both
targets the same theorem would duplicate identity and proof credit.

This intake freezes the received claim, its admissible family, the non-substitution boundary, and
the decisions required before an exact statement can be selected. It leaves the canonical
mathematical statement and Lean target null. The provisional root vector is `[H1, M3, R4]`: the
classical theorem family is recognizable but its exact primary-source statement is unaudited;
pinned mathlib exposes relevant existence and uniqueness interfaces but no combined canonical
target is frozen; and no proof reconstruction exists.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record the open statement and source decisions, while
`task-dag.json` keeps all six downstream phases open. `IntakeProbe.lean` checks only adjacent pinned
APIs. No exact-statement, H0, M0, R0, audit-completion, theorem-completion, or master-acceptance
credit is claimed.
