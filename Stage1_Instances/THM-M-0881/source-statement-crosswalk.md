# Source-statement crosswalk

## Repository record and provenance

`Docs/researches/math_theorems.md:6453-6458` supplies exactly the title `扩展图`, attribution
`众多数学家`, period `20世纪`, gloss `扩展图的存在性与构造`, importance `高`, and status
`已验证`. All six lines entered the repository in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, stable source
identifier, formula, definition, theorem number, proof, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:24035-24060` mechanically projects the same gloss. It explicitly leaves
the precise definitions and premises, proof route, dependent lemmas, equivalent forms, axioms,
machine state, and artifact links as `待补充`. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted`, assigns rank 1035 and the `L0 / rework_required` baseline, and states
`theorem_complete=false`.

## Literal crosswalk

| Repository element | Possible mathematical component | Required Lean component | Intake result |
|---|---|---|---|
| `扩展图` | expander graph under a vertex, edge, conductance, or spectral definition | one exact predicate over a fixed graph model and coefficient domain | subject identified; definition open |
| `存在性` | one graph, graphs of selected orders, infinitely many graphs, or an unbounded family | exact existential/universal binders, index type, size law, degree and expansion constants | no quantifier order or constants supplied |
| `构造` | probabilistic existence, explicit algebraic family, algorithm, or computable generator | an exact family/generator object plus proved well-formedness and expansion properties | construction standard open |
| `众多数学家`, `20世纪` | broad historical attribution | pinpoint primary/authoritative edition and source-to-node map | no source credit |
| `已验证` | untrusted inventory metadata | inspectable human proof and kernel evidence would be required | no H or M credit |

## Cluster crosswalk

The immediately following source records separately name Margulis construction, LPS construction,
Ramanujan graphs, Morgenstern's theorem, and the MSS theorem. They make "expander graphs" the most
plausible English subject translation, but they also establish an ownership boundary: those
specific constructions and spectral-optimality results have their own IDs. No statement, proof, or
status may be imported from them without an explicit typed bridge and separate accepted evidence.

## Missing source-to-statement map

An H0 source crosswalk would have to identify an immutable primary or authoritative edition,
stable identifier, theorem/section/page, incorporated definitions, assumptions, every material
transition and conclusion, dependent source IDs, corrections or errata, and an independent reviewer.
None is present. In particular, the repository does not answer:

- which graph and family model is quantified;
- which expansion boundary or spectrum is measured and how it is normalized;
- which degree, constant, subset cutoff, size, uniformity, and effectiveness conditions apply;
- whether the conclusion is existence, explicit construction, algorithmic generation, or a bundle
  of several results; or
- how empty/small graphs, vacuous subset ranges, and repeated family members are treated.

The provisional human-source classification is therefore `H5`: the received catalog wording is not
yet a stable proposition. This is a classification of the repository target, not a claim that
standard expander theorems are false or open.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded literal query
found no obvious graph-expander, vertex-expansion, edge-expansion, or Cheeger-constant API. Pinned
mathlib does provide nearby substrate in `Mathlib.Combinatorics.SimpleGraph.Finite`,
`Mathlib.Combinatorics.SimpleGraph.AdjMatrix`, and
`Mathlib.Combinatorics.SimpleGraph.LapMatrix`. The intake probe checks representative declarations
from that substrate only.

This is neither an exhaustive absence claim nor the downstream immutable anchor audit. Generic graph
and matrix declarations do not determine the source proposition, an expression fingerprint, a proof
body, or M credit.

## Exact-statement gate

The dependent statement phase is blocked until accountable source selection resolves every row
above. It must then freeze ordered binders, domains and universes, all hypotheses, the exact
conclusion, degenerate cases, minimal pinned imports, an elaborated expression fingerprint, checked
alternate encodings, and the mandated hypothesis/domain/scope/boundary mutations. Intake creates no
canonical mathematical or Lean statement and does not claim that gate.
