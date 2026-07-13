# THM-M-0833 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Four Color Theorem. The catalog
claim says only that planar graphs can be colored with four colors, attributes the result to Appel
and Haken in 1976, and labels it `已验证`. That label is untrusted metadata and supplies no human-
source or machine-proof credit.

## Frozen scope

The recognizable theorem family is preserved: every finite planar simple graph, or equivalently
the adjacency graph of the regions of a simple planar map under a checked representation bridge,
admits a proper coloring using at most four colors. The catalog does not define planarity, finiteness,
the graph/map bridge, loops or parallel edges, map-region adjacency, or boundary conventions.
Those choices are proposition-changing, so this intake does not select a canonical Lean expression.

Georges Gonthier's report *A computer-checked proof of the Four Color Theorem* was inspected as an
authoritative source lead. Section 2 states the simple-planar-map version and defines regions and
adjacency. The associated Rocq/Coq project at immutable commit
`f2fcc837b817632f334f9c7d7fbb0195ad4ba4e2` contains terminal declarations `four_color`,
`four_color_finite`, and `four_color_hypermap`. These records strongly identify the intended family,
but they have not been admitted as a reviewed H0 packet or integrated into this Lean 4 repository.
They therefore provide no M0 or theorem-completion credit.

## Lean boundary

Pinned mathlib defines `SimpleGraph.Coloring`, `SimpleGraph.Colorable`, and chromatic number. Its
coloring module explicitly leaves planar graphs as TODO work, and bounded searches found no planar-
graph predicate or Four Color declaration. `IntakeProbe.lean` authenticates only the coloring side of
a future statement; it neither defines planarity nor states or proves the target.

The provisional root vector is `[H1, M3, R3]`: the mathematical family and a detailed source are
known but exact assumptions and independent review remain open; useful coloring interfaces exist but
the exact Lean target and planar bridge do not; and this dossier maps scope without reconstructing
the proof. All six downstream tasks remain open. No exact Lean statement, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.

