# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6642-6647` supplies exactly the title `Thomassen定理`, attribution
to Carsten Thomassen, year 1994, the gloss `平面图的列表色数`, importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, exact theorem,
definitions, binders, hypotheses, conclusion, proof boundary, correction history, reviewer, or
formal artifact.

`Docs/Stage0_Blueprint.md:24764-24789` repeats the gloss while explicitly leaving precise definitions
and premises, proof process, dependencies, alternate forms, axioms, machine status, and artifact
links open. Its generic claim that a closed result exists is not evidence. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog element | Needed mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Thomassen定理`, 1994 | exact named result, edition, statement, proof, and corrections | immutable source record and node mapping | family identified; primary text not admitted |
| "planar graph" | graph class and planarity or embedding definition | source-approved predicate on `SimpleGraph V` or plane-map structure | absent |
| "list chromatic number" | a list assignment and proper choice from each vertex list | a source-approved `ListColorable` predicate | no pinned mathlib API located |
| implicit bound | five-choosability or list chromatic number at most five | `ListColorable 5` or an inequality with checked equivalence | title metadata identifies five; encoding open |
| `已验证` | primary human proof and kernel receipts would be required | accepted H/M evidence packets | no credit |

The Chinese gloss is recognizable but not binder-complete. It omits the numeral five and does not
settle graph finiteness, simple versus embedded graph structure, list representation and cardinality,
color carrier, planarity witness ownership, or boundary cases.

## Primary-source lead

Crossref and DOI metadata identify the likely primary source as:

> C. Thomassen, *Every Planar Graph Is 5-Choosable*, Journal of Combinatorial Theory, Series B
> 62(1) (September 1994), 180-181, DOI `10.1006/jctb.1994.1062`, PII
> `S0095895684710628`.

The metadata fixes author, title, journal, date, volume, issue, pages, and DOI. Unpaywall reports no
open-access or repository copy. This run therefore did not admit or inspect an immutable copy of
the two primary pages, their exact terminology, incorporated definitions, proof steps, correction
history, or errata. The citation is an H1 source lead, not an H0 packet.

Before H0, an accountable source reviewer must preserve a lawful immutable copy, pinpoint the exact
claim and proof boundary, map every premise and conclusion, audit corrections and errata, justify
the transport into the selected modern graph and list-coloring conventions, and obtain independent
approval.

## Conventional family evidence

The abstract of arXiv `1103.1801v1`, *Graphs with two crossings are 5-choosable*, defines a graph as
`k`-choosable when it can be properly colored whenever every vertex has a list of at least `k`
available colors, then states that Thomassen's theorem says every planar graph is 5-choosable.
The abstract of arXiv `1005.5194v3`, *Thomassen's Choosability Argument Revisited*, independently
says Thomassen (1994) proved every planar graph is 5-choosable.

These are secondary E5 records. They identify the conventional theorem family and expose the
at-least-five convention; they do not freeze the repository's canonical statement or establish H0.

## Statement decisions still open

| Decision | Why it changes the proposition |
|---|---|
| finite graphs versus arbitrary locally finite graphs | changes carriers, instances, and proof scope |
| abstract planar graph versus supplied plane embedding | changes binders and witness ownership |
| simple graph versus plane map or multigraph | changes loop, parallel-edge, face, and connectivity semantics |
| exactly five versus at least five allowed colors | requires a checked finite-list thinning transport |
| finite set, multiset, or duplicate-bearing list | changes cardinality and membership semantics |
| arbitrary color type versus natural-number colors | changes universes and decidable-equality assumptions |
| `ListColorable 5` versus list chromatic number `<= 5` | requires an exact definition and checked equivalence |
| disconnected and degenerate inputs | affects component transport and empty/small-carrier behavior |

## Lean discovery boundary

Pinned `Mathlib.Combinatorics.SimpleGraph.Coloring` defines ordinary proper `Coloring`,
`Colorable`, and `chromaticNumber`; it lists planar graphs as TODO. A bounded search across repo-
local and pinned-mathlib Lean found no obvious Thomassen, choosability, list-coloring, list-
chromatic, or graph-planarity declaration. `IntakeProbe.lean` authenticates only adjacent coloring
interfaces. This is an intake feasibility observation, not an exhaustive anchor audit or a proof of
external absence.

One immutable external lead is `bsniegowski/lean-planar-graphs` at commit
`4d560bc5ec87c763d2042b9e7a5dcfc67b6e6c3d`. Module `LeanPlanarGraphs.Thomassen_1994` declares
`PlanarGraph.fiveListColorable (G : PlanarGraph V) : G.ListColorable 5`. Its `KList` uses exactly
five natural-number colors per vertex, and `PlanarGraph` carries finite connected supplied embedding
data. The theorem source and dependencies contain explicit `sorry` placeholders, and the project
targets Lean `4.30.0-rc2` with another mathlib revision. It is a blocked interface lead, not M1,
M0, or proof evidence; the systematic anchor audit remains downstream.

The canonical module, expression and environment fingerprints, alternate encodings, statement
mutations, and formal-candidate provenance remain null or open. No exact statement, H0, M0, audit
completion, or theorem completion is claimed.
