# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5956-5961` supplies exactly the title `欧拉公式`, attribution
Leonhard Euler, year 1750, gloss `平面图顶点、边、面的关系`, importance high, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no formula, bibliography, edition,
page, theorem locator, definitions, assumptions, proof boundary, corrections, or formal artifact.

`Docs/Stage0_Blueprint.md:22118-22143` projects the record as `THM-M-0810` and labels its kind
"formula / identity," while explicitly leaving the exact definitions and premises, equivalent
forms, logical foundation, axioms, machine status, and artifact links open. The rev-5.6 manifest
retains `已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Primary-source boundary

The catalog attribution and date are bibliographic leads, not a pinpoint source. This intake does
not assign a particular Euler edition, modern translation, theorem/page, or proof to the target.
No immutable primary text was admitted, no incorporated definitions or hypotheses were mapped, and
no correction or erratum search or independent source review was completed. Consequently the
received wording is not promoted to `H0` or even to one reconstructed proposition.

Before source credit, an accountable reviewer must preserve an immutable approved source, identify
the exact statement and every referenced definition, transcribe its equation and ordered premises,
map the proof boundary, inspect corrections and errata, and obtain independent review. A modern
source may clarify terminology, but it must also explain its relationship to the catalog's Euler
attribution and 1750 date.

## Clause crosswalk

| Repository phrase | Mathematical information still required | Prospective Lean surface | Intake result |
|---|---|---|---|
| "planar graph" | plane embedding as data or abstract planarity; finite/simple/multigraph policy | an embedded graph or combinatorial-map structure, not only `SimpleGraph` | absent |
| "vertices" | full carrier versus support; finiteness; isolated vertices | `Fintype.card V` after the carrier is fixed | adjacent API only |
| "edges" | unoriented edges, darts, loops, multiplicity, and finiteness | `SimpleGraph.edgeFinset.card` only for the simple-graph candidate | adjacent API only |
| "faces" | complement components or dart/rotation orbits; outer face; cellularity | a face type with a proved finite cardinality | no pinned candidate located |
| "relationship" | exact equality and connected/disconnected correction | one source-identical `Prop` | formula absent |
| Euler / 1750 | exact work, edition, passage, genealogy, and corrections | source provenance only | bibliographic lead |
| `已验证` | claimed formalization status | accepted kernel evidence would be required | explicitly rejected |

## Lean discovery boundary

`IntakeProbe.lean` imports only
`Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected`, which transitively exposes the finite
graph API used by the probe. It checks `SimpleGraph`, `SimpleGraph.edgeSet`,
`SimpleGraph.edgeFinset`, `SimpleGraph.Connected`, `SimpleGraph.ConnectedComponent`, and
`Fintype.card`. These declarations elaborate under the pinned Lean 4 and mathlib revisions.

A bounded case-insensitive search over pinned `Mathlib.Combinatorics.SimpleGraph` for graph
planarity, plane graphs, face counts, and the Euler formula found no target-specific interface. A
separate repo-local Lean search found only unrelated uses of "planar." These searches are intake
reconnaissance, not a frozen discovery protocol, exhaustive external anchor audit, or absence proof.
No declaration or proof body receives target credit.

## First blocker

The dependent statement phase is blocked until an immutable, independently reviewed source selects
one exact equation and fixes embedding data, graph class, connectedness, face convention,
plane/sphere/surface scope, ordered binders, hypotheses, conclusion, and degenerate cases. Only then
may it build any missing embedded-graph infrastructure, minimize imports, elaborate and serialize
the exact target, compile credited transports, and run the required statement mutations.
