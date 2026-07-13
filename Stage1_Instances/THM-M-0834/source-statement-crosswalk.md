# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6124-6129` supplies exactly the title `五色定理`, attribution to
Percy Heawood, year 1890, the gloss `平面图可用五种颜色着色`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable theorem ID,
definition, binder, hypothesis, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22766-22791` repeats the gloss while explicitly leaving exact definitions
and premises, proof process, dependencies, alternate forms, axioms, machine status, and artifact
links open. Its generic planning text about a known result is not proof evidence. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog element | Needed mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| "planar graph" | exact graph class and planarity/embedding definition | a source-approved predicate on `SimpleGraph V` or a plane-map structure | absent |
| "can be colored" | proper vertex or map-region coloring, with all adjacency conventions | `SimpleGraph.Coloring` / `SimpleGraph.Colorable` or checked alternate encoding | adjacent API only |
| "five colors" | at most five versus exactly five; finite palette convention | `Fin 5`, `G.Colorable 5`, or `G.chromaticNumber <= 5` | relationship not frozen |
| Percy Heawood, 1890 | exact edition, statement, definitions, proof, and corrections | immutable source record and node mapping | bibliographic lead only |
| `已验证` | source proof and kernel receipts would be required | accepted H/M evidence packets | no credit |

The Chinese gloss is recognizable but not binder-complete. It does not decide whether a plane
embedding is input or merely exists, whether the graph is finite and simple, or whether map regions
rather than vertices are colored.

## Historical source lead

Standard bibliographic histories identify the original proof source as:

> P. J. Heawood, *Map-Colour Theorem*, Quarterly Journal of Pure and Applied Mathematics 24
> (1890), 332-338.

This is a primary-source lead, not an admitted H0 packet. No stable lawful copy of the primary text
was preserved in the dossier, and its exact theorem passage, incorporated definitions, assumptions,
proof steps, correction history, and errata were not inspected and independently reviewed. A
publisher metadata search also surfaced Heawood's later paper with the same title, *Proceedings of
the London Mathematical Society* s2-51 (1949), 161-175, DOI
`10.1112/plms/s2-51.3.161`; that later higher-surface result must not be mistaken for the 1890
plane five-color proof.

The citation was independently confirmed by zbMATH's stable record `2689944`, JFM identifier
`22.0562.02`. Its contemporary German review describes the target in map language: plane regions
that share a boundary line must receive different colors. It reports that Heawood invalidates
Kempe's simultaneous color-interchange step and improves the simple-case upper bound from six to
five while leaving four unresolved. This is valuable family and boundary evidence, especially for
point-contact and map-to-graph decisions, but remains a secondary review rather than inspection of
the primary pages.

Before H0, an accountable source reviewer must pin and inspect the 1890 edition, identify the exact
statement and its map/graph definitions, map every premise and conclusion, locate the complete proof
boundary and dependencies, audit corrections and errata, explain the transport to a modern planar
simple-graph statement, and obtain independent approval.

## Statement decisions still open

| Decision | Why it changes the target |
|---|---|
| finite simple graph versus plane map | changes carriers, adjacency, and finiteness assumptions |
| supplied embedding versus existential planarity | changes binders and witness ownership |
| plane versus sphere | requires a checked topological or combinatorial transport |
| proper vertex coloring versus region coloring | requires graph duality and treatment of bridges/faces |
| `Colorable 5` versus chromatic number at most five | requires exact API equivalence and coercion checks |
| at most five versus all five used | the latter is false for small graphs unless qualified |
| disconnected and degenerate inputs | affects induction, embedding, and empty-type behavior |

## Lean discovery boundary

Pinned `Mathlib.Combinatorics.SimpleGraph.Coloring` gives an exact meaning to ordinary proper graph
coloring and to `Colorable n`. `IntakeProbe.lean` elaborates those interfaces. The same module lists
planar graphs as TODO; mathlib's thousand-theorem index names the five-color theorem without a
declaration; and a bounded repository/pinned-dependency search found no exact-topic declaration.
This supports a provisional M4 classification only; it is neither an exhaustive formal candidate
audit nor proof that no external Lean artifact exists.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, statement mutations, and formal candidate provenance remain null. No exact
statement, H0, M0, audit completion, or theorem completion is claimed.

One external Lean 4 lead is known: `https://github.com/bsniegowski/lean-planar-graphs` at commit
`4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d`. Its `PlanarGraph.fiveColorable` declaration derives
ordinary five-colorability from a list-coloring theorem, but that theorem and multiple core
dependencies contain explicit `sorry` placeholders. The project also targets Lean `4.30.0-rc2` and
a different mathlib revision. This is a blocked discovery lead, not M1, M0, or proof evidence; the
systematic immutable anchor audit remains downstream.
