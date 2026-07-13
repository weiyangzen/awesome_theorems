# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0834`, the title `五色定理` (five-color theorem), attribution
to Percy Heawood, the year 1890, and the gloss `平面图可用五种颜色着色` (planar graphs can be colored
using five colors). Intake preserves this classical graph-coloring family without manufacturing
the missing mathematical conventions.

## Candidate scope, not credited

A familiar modern formulation is: every finite planar simple graph admits a proper vertex coloring
with at most five colors. With a source-approved planarity predicate `IsPlanar`, the colorability
conclusion could use pinned mathlib's `G.Colorable 5`, which abbreviates a nonempty type of graph
homomorphisms from `G` to the complete graph on `Fin 5`.

This description is a resolution candidate only. There is no selected planarity encoding, exact
human statement, Lean expression, or proof at intake.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted immutable source:

- finite graphs only, arbitrary graphs with a finiteness hypothesis, or a locally finite extension;
- simple loopless undirected graphs, multigraphs, plane maps, regions of a map, or another carrier;
- graph planarity as existence of a crossing-free embedding, a fixed combinatorial embedding,
  forbidden-minor characterization, inductive plane graph, or map duality;
- whether the embedding is in the plane or sphere and whether disconnected components, bridges,
  repeated face boundaries, isolated vertices, and the outer face are represented;
- proper vertex coloring versus map-region coloring, and `at most five`, `Colorable 5`, existence of
  a function into `Fin 5`, or a chromatic-number inequality;
- ordered binders, required finiteness and decidability instances, and any use of classical choice;
- exact source edition, theorem or page locator, definitions, proof boundary, corrections and
  errata, complete premise/conclusion map, and independent review; and
- checked transports among plane-map, plane-graph, abstract-planar-graph, `Colorable 5`, and
  chromatic-number formulations.

These choices affect the proposition. The familiar finite-simple-graph wording cannot be silently
installed merely because it is standard in a modern textbook.

## Boundary cases

No case is excluded at intake. Source review must decide empty and singleton vertex types, edgeless
and disconnected graphs, isolated vertices, bridges, graphs with fewer than five vertices, loops
or parallel edges in a map encoding, and embeddings with degenerate faces. It must also distinguish
using at most five colors from requiring all five colors to appear.

## Explicit exclusions

- The four-color theorem, a four-color formalization, or its stronger conclusion used as a
  substitute without an explicit checked and source-approved bridge.
- Heawood's higher-genus map-color theorem, the Heawood number, or a surface-coloring result.
- A plane-map theorem substituted for an abstract planar-graph theorem, or conversely, without
  verified duality and embedding transports.
- A graph structure that assumes the desired coloring, or a theorem that takes `G.Colorable 5` as
  a premise and merely returns it.
- The six-color theorem, a bounded-degree theorem, or another weaker graph class.
- A finite search, SAT result, drawing heuristic, or unchecked coloring algorithm.
- The catalog label `已验证` as human-source or Lean kernel evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Coloring` supplies `SimpleGraph.Coloring`,
`SimpleGraph.Coloring.mk`, `SimpleGraph.Colorable`, `SimpleGraph.Colorable.mono`,
`SimpleGraph.chromaticNumber`, and `SimpleGraph.chromaticNumber_le_iff_colorable`. The module's TODO
list includes planar graphs. A bounded case-insensitive search across repo-local Lean and pinned
dependencies found no five-color, Heawood, map-color, or graph-planarity declaration. Mathlib's
`docs/1000.yaml` contains the title "Five color theorem" without a `decl` field. This is an intake
feasibility observation, not an exhaustive anchor audit or a formal absence theorem.

An external discovery lead, `bsniegowski/lean-planar-graphs` at immutable commit
`4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d`, defines a combinatorial `IsPlanar` and declares
`PlanarGraph.fiveColorable`. Its proof passes through `PlanarGraph.fiveListColorable` and many
explicit `sorry` placeholders, and the project uses Lean `4.30.0-rc2` rather than this repository's
pinned toolchain. It is a useful interface lead only, not a usable formal anchor or proof.
