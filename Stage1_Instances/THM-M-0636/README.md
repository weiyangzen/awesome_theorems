# THM-M-0636 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for catalog target `THM-M-0636`,
`不动点定理` (fixed-point theorem). The repository gives the gloss `紧凸集上连续映射有不动点`
(a continuous map on a compact convex set has a fixed point), attributes it to Luitzen Brouwer in
1910, and labels it `已验证`. Under rev-5.6 that label is untrusted metadata, not human-source or
kernel evidence.

The attribution and neighboring catalog entries identify the Brouwer compact-convex family, but the
gloss is not binder-complete. It omits the ambient scalar and space, finite-dimensionality,
nonemptiness, the self-map condition, the topology used for continuity, and the exact fixed-point
conclusion. Without a finite-dimensional or comparable hypothesis, the wording can instead suggest
stronger Schauder or Tychonoff variants. Choosing one familiar formulation at intake would add
mathematics that the source record does not state.

`IntakeProbe.lean` checks only adjacent pinned convexity, compactness, continuity, self-map, finite-
dimensional, and fixed-point APIs. A bounded name search found no Brouwer compact-convex terminal
declaration in pinned mathlib. These are discovery observations, not the downstream anchor audit.

The provisional root vector is `[H1, M4, R4]`: a classical published theorem family is identified,
but no pinpoint source proposition, exact Lean target, or readable proof reconstruction is accepted.
`instance.json` is the structured scope authority, the scope map and crosswalk freeze the unresolved
choices and duplicate boundaries, and all six downstream phases remain open in `task-dag.json`. No
H0, M0, R0, accepted proof state, audit completion, theorem completion, or master acceptance is
claimed.
