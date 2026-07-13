# THM-M-0880 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6446-6451` supplies exactly the title `稀疏割`, the attribution
`众多数学家`, the period `20世纪`, the gloss `图划分的稀疏性`, importance "high," and status
`已验证`. All six uncited lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, ordered binder, hypothesis, conclusion, proof, correction record, or formal artifact.

`Docs/Stage0_Blueprint.md:24008-24033` mechanically projects the same gloss. It explicitly leaves
the formal system, foundations, exact definitions and premises, proof route, dependent lemmas,
equivalent forms, axioms, machine status, and artifact links as `待补充`. The rev-5.6 manifest
preserves `已验证` only as `source_status_untrusted`, assigns rank 1433 and the
`L0 / rework_required` baseline, and states `theorem_complete=false`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `稀疏割` | sparse/sparsest cut, conductance, edge expansion, balanced separator, or another low-boundary partition notion | one exact predicate or optimization objective over a fixed graph/weight model | subject identified; theorem identity open |
| `图` | finite simple, weighted, directed, multi-, capacity, or capacity-plus-demand graph | carrier, graph structure, finiteness/decidability instances, weight functions and coefficient types | absent |
| `划分` | a subset and complement, ordered/unordered bipartition, or multi-part partition | exact cut representation and nonempty/proper/balance hypotheses | absent |
| `稀疏性` | crossing capacity divided by cardinality, product, minimum volume, separated demand, or another normalization | numerator, denominator, division convention, positivity and zero-case rules | absent |
| many mathematicians / twentieth century | broad historical provenance | immutable pinpoint source, theorem/section/page, assumptions, corrections, and reviewer | no source credit |
| `已验证` | catalog status metadata | accepted human-source proof and kernel receipts would be required | no H or M credit |

## Neighbor and duplicate-topic crosswalk

The catalog separately owns broad network, minimum-cost, and multicommodity-flow topics
(`THM-M-0877` through `THM-M-0879`), maximum-flow/minimum-cut (`THM-M-0814`), Karger's and
Stoer-Wagner's global-minimum-cut algorithms (`THM-M-0831`, `THM-M-0832`), expander graphs
(`THM-M-0881`), spectral graph theory (`THM-M-0887`), and Cheeger inequality (`THM-M-0888`).
These establish that flow, global cut, expansion, and spectral relationships are not automatically
part of this root.

`Docs/researches/cs_theorems.md:138`, projected as `THM-C-0077` in Stage0, independently lists the
Arora-Rao-Vazirani theorem with the
gloss `稀疏割的O(√log n)近似`. That record gives a plausible algorithmic theorem family, but it
has a different catalog identity, attribution, date, status, and subject category. The broad
`THM-M-0880` record does not cite it. Importing its approximation factor would therefore be an
unsupported narrowing, not a source crosswalk.

## Non-substitution boundary

A minimum-cut theorem minimizes crossing capacity without the usual sparse-cut normalization. A
conductance or edge-expansion theorem chooses a volume/cardinality convention. A balanced separator
adds a balance condition. The uniform and nonuniform sparsest-cut problems use different
denominators, and an approximation theorem additionally fixes an algorithmic and complexity model.
None can be substituted for another from the received gloss alone.

## Source gate

Before this target can leave `H5`, accountable reviewers must redirect the gloss to one immutable,
truth-valued proposition; preserve a primary or authoritative source; freeze every graph, weight,
cut, objective, denominator, positivity, balance, algorithm, complexity, and boundary convention;
map every premise and conclusion to a theorem/section/page locator; inspect correction history; and
justify why the proposition represents `THM-M-0880`. A qualified independent reviewer must approve
the mapping. Human-proof status must then be classified afresh rather than inherited from
`已验证`.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean`
checks adjacent interfaces for edge sets/finsets, induced subgraphs, degrees, deleted-edge
connectivity, interedges/edge density, and graph-coloring partitions. `SimpleGraph.edgeDensity`
uses the denominator `|S| * |T|`; it is adjacent density substrate, not a selected sparse-cut
objective or optimization theorem. The `SimpleGraph.Partition` API is explicitly a
partition into independent color classes, not a sparse cut. A bounded search over repo-local Lean
and pinned mathlib found no exact sparse-cut, sparsest-cut, conductance, Cheeger-constant, or
edge-expansion declaration. This is intake discovery only, not the downstream immutable anchor
audit or a claim about all Lean projects.

The canonical module, expression, expression hash, environment fingerprint, checked transports,
and statement mutations remain null. No H0, M0, R0, audit completion, or theorem completion is
claimed.
