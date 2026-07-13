# THM-M-0307 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `迹定理`
(`trace theorem`). The catalog supplies only the gloss `Sobolev函数在边界上的限制` (restriction
of Sobolev functions to the boundary), the attribution Sergei Sobolev, the year 1936, and an
untrusted `已验证` label. Those words identify a classical theorem family, but not one stable
truth-valued proposition.

A trace statement must fix the domain and boundary regularity, Sobolev order and exponent,
representative semantics, boundary measure, trace codomain, parameter range, boundedness estimate,
and whether it also asserts uniqueness, surjectivity, a right inverse, or a kernel characterization.
Intake does not choose a familiar Lipschitz-domain variant from memory or replace the target by
pointwise restriction of smooth functions.

The provisional catalog-target vector is `[H5, M4, R4]`. `H5` classifies the received wording as
not yet a stable proposition; it does not say that source-selected Sobolev trace theorems are false
or open. No exact usable Lean target or source-faithful readable proof can attach before statement
selection. `IntakeProbe.lean` authenticates only adjacent pinned `Lp`, measure restriction,
manifold-boundary, and Gagliardo-Nirenberg-Sobolev APIs. It declares no theorem and provides no
proof credit.

`instance.json` is the structured scope authority. `scope-map.md` freezes proposition-changing
choices and exclusions, `source-statement-crosswalk.md` records provenance and the unresolved
source mapping, and `task-dag.json` leaves all six downstream phases open. This is a self-tested
worker proposal only. No canonical statement, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
