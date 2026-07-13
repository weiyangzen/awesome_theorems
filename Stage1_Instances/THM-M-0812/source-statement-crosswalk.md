# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5970-5975` supplies the title `柯尼希定理`, attribution Denes
Konig, year 1931, and the claim `二部图中最大匹配等于最小顶点覆盖`. Git history traces all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` and source blob
`5c1de0c2bda67f7257142dd99b0dd91d69e0a3bf`.

`Docs/Stage0_Blueprint.md:22172-22197` repeats the claim but leaves precise definitions and
premises, proof route, alternate forms, axioms, machine state, and artifact links open. The
rev-5.6 manifest gives execution rank 1371 and resets the target to `L0 / rework_required`; its
`source_status_untrusted` value gives no assurance credit.

## Translated primary-text lead

The inspected source is Gabor Szarnyas, *Graphs and matrices: A translation of "Graphok es
matrixok" by Denes Konig (1931)*, arXiv:`2009.03780v1` (2020). The observed three-page PDF is
94,803 bytes with SHA-256
`cecbda9a56b360c5f588c2db30d58d22f1cf0af3333ab009521a4c4ac8ff671a`. The extracted arXiv
source `ms.tex` is 9,171 bytes with SHA-256
`c64b81e2a348aea280f96a7dd32a09b5a0bd6283f314821733d95a76a9f453d4`.

The translation says the talk was given on March 26, 1931 and the Hungarian paper appeared in
*Matematikai es Fizikai Lapok* 38 (1931). The REAL-J record 7307 identifies that volume and lists
`Konig Denes: Graphok es matrixok`; its observed metadata HTML has SHA-256
`e2d0e7dd5ae21fbdc0ba228a4cfd04497db154b14aa8a418c776b9bad584db98`. The 95 MB original
volume PDF was not successfully preserved and inspected, so intake makes no original-language or
translation-fidelity claim.

In the translation, page 1 begins "Let G be a (finite) bipartite graph," defines `M` as the maximum
number of edges with no common vertex, and defines covering vertices as vertices incident to all
edges. Pages 1-2 construct a cover of `M` vertices from a maximum matching. Page 3 states:

> In a bipartite graph, the minimal number of vertices covering all edges is equal to the maximal
> number of edges which do not have a common vertex.

This is a direct statement and proof match for the catalog claim. It supports `H1`, not `H0`: the
original Hungarian statement and proof were not inspected; translation fidelity, correction and
errata status, incorporated-definition mapping, source-to-obligation coverage, durable admission,
and independent graph-theory/source review remain open.

## Proof-boundary crosswalk

| Source component | Human meaning | Formal component | Current status |
|---|---|---|---|
| finite bipartite `G` | finite graph with two vertex sides and only cross-edges; parallel-edge convention unstated | finite `L`, `R`, `E` and endpoint maps `left : E -> L`, `right : E -> R` | exact incidence binders frozen; parallel edges preserved |
| `M` disjoint edges | maximum-cardinality matching, counted by edges | `IsEdgeMatching` plus attained/universally bounded `HasMatchingNumber` | exact edge-count extremum elaborated |
| vertices covering edges | every graph edge has an endpoint in the set | `IsBipartiteVertexCover` plus attained/universally bounded `HasVertexCoverNumber` | exact typed-side cover extremum elaborated |
| no augmenting `K`-path | a maximum matching admits no alternating path between unmatched opposite-side vertices | alternating-path lemma and cardinality contradiction | source proof lead only |
| selected endpoint set | choose one endpoint of each matched edge according to alternating reachability | construct a vertex cover of matching size | four-case source proof lead only |
| four cases | endpoints unmatched/matched on their respective sides | exhaustive endpoint-membership split proving every edge is covered | not yet an obligation registry |
| reverse inequality | a cover must meet every pairwise disjoint matching edge at distinct vertices | matching size is at most every cover size | easy but still required composition child |
| equality | minimum cover size equals maximum matching edge count | `KonigMatchingCoverTarget` with one shared extremal `k` | canonical root elaborated and fingerprinted |
| matrix result | rows/columns covering nonzero entries versus entries in distinct rows/columns | bipartite incidence-matrix corollary | excluded alternate until separately transported |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Combinatorics.SimpleGraph.Bipartite` defines `SimpleGraph.IsBipartite` and
  `SimpleGraph.IsBipartiteWith`.
- `Mathlib.Combinatorics.SimpleGraph.Matching` defines
  `SimpleGraph.Subgraph.IsMatching`; its matching is a subgraph, and the source includes
  support-to-edge interfaces such as `IsMatching.toEdge` and its surjectivity.
- `Mathlib.Combinatorics.SimpleGraph.VertexCover` defines `SimpleGraph.IsVertexCover` and the
  `ENat`-valued infimum `SimpleGraph.vertexCoverNum`, with `vertexCoverNum_exists` providing a
  realizing cover.
- `Mathlib.Combinatorics.SimpleGraph.Hall` provides
  `SimpleGraph.exists_isMatching_of_forall_ncard_le`, a Hall-theorem interface rather than the
  Konig equality.

The bounded repo-local and pinned-mathlib search found no exact matching-cover equality and no
maximum matching-number definition. That is discovery evidence only, not a global absence claim or
the downstream immutable anchor audit. `IntakeProbe.lean` checks the listed interfaces against the
pinned toolchain but owns no theorem, wrapper, transport, or proof body.

## Statement resolution

`Stage1Instances.THM_M_0812.KonigMatchingCoverTarget` now supplies the exact finite incidence
encoding. `konigMatchingCoverTarget_iff_expanded` checks its direct binder-complete expansion, and
`konigMatchingCoverTarget_iff_simpleRelationKonigTarget` proves that erasing parallel-edge identity
preserves both extrema. Four structural mutations distinguish removed finiteness, changed matching
cardinality, changed binder scope, and an excluded edgeless boundary; the edgeless and single-edge
cases are kernel-checked separately. The exact hashes, imports, and environment are recorded in
`statement.json` and `statement-validation.md`.

Before H0, accountable reviewers must still inspect the original-language source, verify every
translated premise and inference, audit corrections and errata, map the proof to stable
obligations, and independently approve the packet. This statement resolution gives no proof,
anchor-audit, H0, M0, R0, audit-completion, or theorem-completion credit.
