# THM-M-0904 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `Dinitz猜想`
(Dinitz conjecture). The catalog supplies Jeff Dinitz, the year 1979, and only the gloss
`列表着色的存在性` (existence of list coloring). Stage0 explicitly leaves the precise definitions
and hypotheses open. Those fields identify a famous problem family, but they do not select one
binder-complete proposition.

The usual array formulation starts with an `n x n` array of color lists and asks for one entry from
each list so that chosen colors are distinct within every row and every column. Material choices
remain unresolved: lists of exactly `n` colors versus at least `n`; finite sets versus duplicate-
bearing lists; arbitrary color carrier versus a finite palette; whether `n = 0` is included; and
whether the canonical target is the array statement, the equivalent list edge-coloring statement
for `K_(n,n)`, or Fred Galvin's strictly stronger bipartite-multigraph theorem.

The neighboring repository target `THM-M-0905` is named "Galvin theorem" and glossed "proof of the
Dinitz conjecture." That boundary makes it especially important not to substitute the stronger
bipartite-multigraph theorem for this target during intake. Galvin's 1995 paper is a bibliographic
source lead, not a selected canonical statement. A later 1996 abstract independently states the
stronger result as: every `k`-edge-colorable bipartite multigraph is `k`-edge-choosable. Neither
source has been admitted as an exact H0 source for this target.

`IntakeProbe.lean` checks only adjacent pinned mathlib interfaces: simple-graph coloring,
bipartiteness, complete bipartite graphs, and line graphs. A bounded search found line-graph and
ordinary vertex-coloring infrastructure but no list-coloring or Dinitz/Galvin declaration. The
probe and search are intake feasibility observations, not an anchor audit or proof.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the catalog wording as not yet one
stable proposition; it does not claim the mathematical conjecture is false or open. The canonical
human and Lean statements remain null, and all downstream tasks remain open. No H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
