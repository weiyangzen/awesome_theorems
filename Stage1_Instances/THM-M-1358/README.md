# THM-M-1358 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `分岔理论`
(bifurcation theory). The catalog supplies only that name, a collective twentieth-century
attribution, and the gloss `参数变化导致的定性变化` (qualitative changes caused by varying a
parameter). It supplies no cited proposition, definitions, hypotheses, conclusion, or proof
source. Its `已验证` status is explicitly untrusted metadata under rev-5.6.

Bifurcation theory is a field, not one theorem. The gloss may describe bifurcations of equilibria,
periodic orbits, invariant sets, maps, or flows; local or global changes; and persistence,
existence, classification, or genericity results under different equivalence and nondegeneracy
notions. The neighboring catalog entries separately own saddle-node, Hopf, transcritical, and
pitchfork bifurcations. Selecting any familiar member of that family from memory would silently
substitute a new target.

This intake freezes the ambiguity rather than inventing missing mathematics. The provisional root
vector is `[H5, M4, R4]`. `H5` records that the supplied field label and phenomenon gloss are not
yet a stable truth-valued proposition; it does not say that standard bifurcation theorems are false
or open. No source-identical usable Lean artifact or source-faithful proof reconstruction can be
attached before a proposition is selected.

Gerald Teschl's *Ordinary Differential Equations and Dynamical Systems*, Section 6.5, was inspected
as an authoritative discovery lead. It uses almost the catalog's gloss to introduce the field,
then gives separate pitchfork, transcritical, and saddle-node examples and an implicit-function
necessary condition. The author expressly declines to develop the theory there. The repository
does not cite this book or select any of those examples or claims, so none is accepted as the root.

`IntakeProbe.lean` checks only adjacent pinned implicit-function, ODE, flow, fixed-point, derivative,
and smoothness APIs. It states no bifurcation theorem and receives no statement or proof credit.
The structured scope authority is `instance.json`, the resolution boundary is in `scope-map.md`,
the literal source crosswalk is in `source-statement-crosswalk.md`, and all six downstream phases
remain open in `task-dag.json`.

The lifecycle is `planned`. No canonical Lean expression, H0, M0, R0, accepted execution state,
audit completion, theorem completion, or master acceptance is claimed.
