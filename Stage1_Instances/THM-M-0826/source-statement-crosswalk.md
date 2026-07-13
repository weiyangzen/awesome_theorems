# THM-M-0826 source-statement crosswalk

## Repository source and provenance

The complete upstream record is `Docs/researches/math_theorems.md:6068-6073`:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `Bellman-Ford算法` | names an algorithm family |
| proposer | `Richard Bellman/Lester Ford` | historical attribution only |
| time | `1958` | bibliographic lead only |
| statement | `带负权边的最短路径算法` | topic and capability gloss, not a proposition |
| importance | `高` | scheduling metadata only |
| formalization status | `已验证` | explicitly untrusted; no H/M credit |

All six lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no bibliography, edition,
page, theorem, graph or algorithm definitions, binders, assumptions, conclusion, proof, correction
record, or formal artifact. `Docs/Stage0_Blueprint.md:22550-22575` repeats the gloss while
expressly leaving the definitions and premises, proof path, dependencies, foundation, axioms,
machine status, and artifact links open.

`Docs/researches/cs_theorems.md:167` contains a second inventory row. It says `含负权边的最短路径算法`,
attributes the item to `Bellman, Ford`, records the inconsistent date `1958-56`, and again labels it
verified. This is corroborating inventory metadata, not a source citation. The chronology mismatch
must be resolved rather than silently normalized.

## Historical and modern source leads, not H0 evidence

1. Richard Bellman, "On a routing problem," *Quarterly of Applied Mathematics* 16(1) (1958),
   87-90, DOI `10.1090/qam/102435`. Crossref metadata observed on 2026-07-13 confirms this
   bibliographic identity; Semantic Scholar points to the publisher PDF. The publisher returned
   HTTP 403/520 to this worker, so the exact algorithm, statement, assumptions, proof, and
   corrections were not inspected.
2. Srini Devadas, *6.006 Introduction to Algorithms, Fall 2011, Lecture 17: Shortest Paths III:
   Bellman-Ford*, MIT OpenCourseWare, six-page lecture handout. The observed PDF states the
   relaxation algorithm, gives a theorem that in a graph with no negative-weight cycles the final
   estimates equal the single-source shortest-path weights, sketches the `|V|-1`-pass proof, and
   gives a reachable-negative-cycle detection corollary.
3. Lester R. Ford Jr.'s 1956 RAND paper commonly associated with the algorithm is a historical
   lead suggested by the catalog's second author and inconsistent `1958-56` inventory date. No
   exact edition or passage was obtained or credited in this intake.

The MIT handout is a concrete statement-and-proof lead but is not the catalog's cited source (the
catalog has none), and its theorem says no negative-weight cycles without freezing the finer
reachable-cycle and per-vertex boundary needed for a canonical root. It also does not select
whether path reconstruction, cycle detection, or complexity belongs to the target. No source has
been immutably admitted or independently reviewed; hence these leads do not clear `H5` for the
received non-proposition and do not establish `H0` for any selected theorem.

## Source-to-statement crosswalk

| Catalog element | Mathematical information actually fixed | Lean information required | Result |
|---|---|---|---|
| `Bellman-Ford算法` | repeated-relaxation shortest-path algorithm family | exact recurrence or executable program and state invariant | family only; open |
| `带负权边` | negative edge weights are permitted | ordered additive weight type, infinity/unboundedness model, cycle premise | domain boundary incomplete |
| `最短路径` | intended weighted shortest-path task | graph/path definitions, reachability, infimum/minimum and witness contract | output semantics open |
| Richard Bellman/Lester Ford | historical attribution | admitted editions, precise passages, chronology and source-node map | leads only |
| 1958 | Bellman publication year | relationship to Ford's 1956 work and exact target source | unresolved |
| `已验证` | metadata screening claim | accepted source review or kernel receipt | no credit |

The literal gloss has no connective or conclusion whose truth Lean can check. It fixes neither a
complete algorithm nor what must be proved about it. Consequently no ordered binder, hypothesis,
conclusion, canonical expression, alternate encoding, or expression hash can be populated
truthfully at intake.

## Non-equivalent candidate statement families

| Candidate | Material choices not supplied by the catalog | Intake decision |
|---|---|---|
| distance correctness | source, reachability, infinity, relevant negative-cycle premise, recurrence and final estimate | not selected |
| predecessor/path correctness | tie rules, predecessor representation, witness reconstruction and validity | not selected |
| negative-cycle detection | reachable/global/per-target scope and soundness/completeness direction | not selected |
| termination and pass bound | precise loop, early stopping and finite graph/edge schedule | not selected |
| `O(|V||E|)` complexity | data structure, input encoding, primitive operations and cost model | not selected |
| executable refinement | implementation language/state, arithmetic, overflow and reference relation | not selected |

These statements are not interchangeable. In particular, distance correctness under a no-cycle
premise does not establish a cycle detector or a runtime bound, and generic relaxation invariants
do not identify one concrete implementation.

## Pinned Lean substrate boundary

`IntakeProbe.lean` checks generic operations from
`Mathlib.Combinatorics.Digraph.Basic` and `Mathlib.Combinatorics.Quiver.Path.Weight`:
`Digraph`, `Digraph.Adj`, dependent quiver paths, path length, additive path weight, and additive
weight behavior under nil, cons, and composition. The additive interface accepts an arbitrary
`AddMonoid`, so future source-selected integer-weight models are not excluded by this probe.

These declarations do not define relaxation, a distance table, a minimum over paths, negative
cycles, Bellman-Ford execution, or any correctness or complexity result. A bounded case-insensitive
search for `Bellman-Ford`, `Bellman Ford`, and combined negative-weight/shortest-path phrases found
no occurrence in repo-local Lean or pinned mathlib. This is discovery evidence with a bounded query
list, not an exhaustive absence claim or the downstream anchor audit.

## Source exit gate

Before statement execution, an independent algorithms reviewer must approve a lawful immutable
source edition, pinpoint result and proof boundary, all incorporated definitions, assumptions and
corrections, and a row-by-row mapping to one canonical mathematical claim. The review must also
settle Bellman/Ford chronology and the exact negative-cycle, output, and complexity boundary. Only
then may the statement phase freeze the exact Lean expression, imports, environment fingerprint,
transports, and required mutations. Until that gate passes, the honest classification is
`[H5, M4, R4]`, and all proof, audit, and completion claims remain open.
