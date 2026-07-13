# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0908`, title `Thomassen定理`, attribution to Carsten Thomassen,
year 1994, and the gloss `平面图的列表色数`. Intake preserves the classical planar-graph
five-choosability family without manufacturing its missing mathematical conventions.

This target is distinct from `THM-M-0834`, the ordinary five-color theorem. Five-choosability is
strictly stronger than ordinary five-colorability: the allowed palette may vary by vertex.

## Candidate scope, not credited

A familiar modern formulation is: every finite planar simple graph is 5-choosable. Concretely, for
every assignment of a finite set of at least five available colors to each vertex, there exists a
proper vertex coloring choosing an available color at every vertex.

This is a resolution candidate only. There is no source-approved graph class, planarity encoding,
list representation, canonical human statement, Lean expression, or proof at intake.

## Proposition-changing decisions

The statement phase must freeze all of the following from an admitted immutable source:

- finite graphs only, arbitrary graphs with a finiteness hypothesis, or a locally finite extension;
- simple loopless undirected graphs, multigraphs, plane maps, or another carrier;
- graph planarity as an existential crossing-free embedding, supplied combinatorial embedding,
  forbidden-minor characterization, or another checked representation;
- plane versus sphere, connected versus disconnected graphs, bridges, isolated vertices, and any
  componentwise transport;
- list assignments as finite sets, lists, or multisets, including duplicate semantics;
- list size exactly five versus at least five, and the checked direction of any thinning bridge;
- arbitrary color carrier versus natural numbers, universe level, decidable equality, and whether
  one finite global palette is required;
- proper vertex coloring from the assigned lists versus a list-chromatic-number inequality;
- exact ordered binders, required finiteness and decidability instances, and choice principles;
- source edition, theorem/page locator, definitions, proof boundary, corrections, errata, complete
  premise/conclusion map, and independent review; and
- checked transports among abstract-planar, supplied-plane, exact-list, lower-bound-list, and
  list-chromatic-number formulations.

These choices affect the proposition. The familiar finite-simple-graph wording cannot be silently
installed merely because it is standard in secondary literature.

## Boundary cases

No case is excluded at intake. Source review must decide empty and singleton vertex types, edgeless
and disconnected graphs, isolated vertices and bridges, empty color types, lists of insufficient
size, duplicate-bearing lists, graphs with fewer than five vertices, and embeddings with degenerate
faces. It must ensure that "five" bounds every vertex list rather than requiring five colors to be
used globally or surjectively.

## Explicit exclusions

- `THM-M-0834` ordinary five-colorability or its future receipt used as a substitute; it is weaker.
- The four-color theorem, six-color theorem, bounded-degree theorem, or another coloring result.
- A supplied connected plane-graph theorem substituted for all abstract planar graphs without
  checked embedding and component transports.
- An exactly-five list theorem substituted for an at-least-five convention without checked thinning.
- A graph structure, hypothesis, or field that assumes the desired list coloring.
- A finite search, SAT result, drawing heuristic, or unchecked coloring algorithm.
- The catalog label `已验证`, a bibliography entry, or an API probe as human-source or kernel proof.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.Combinatorics.SimpleGraph.Coloring` supplies ordinary `SimpleGraph.Coloring`,
`SimpleGraph.Colorable`, `SimpleGraph.Colorable.mono`, `SimpleGraph.chromaticNumber`, and
`SimpleGraph.chromaticNumber_le_iff_colorable`. It supplies no located list-coloring or planar-graph
predicate and lists planar graphs as TODO. This is adjacent substrate only.

The external `lean-planar-graphs` candidate at immutable commit
`4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d` supplies useful list-coloring and plane-graph interface
shapes, but its Thomassen proof contains placeholders, narrows the scope, and uses an incompatible
toolchain. It provides no proof credit. Exact candidate inventory and provenance remain the later
anchor-audit phase.
