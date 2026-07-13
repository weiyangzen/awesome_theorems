# Source-statement crosswalk

## Repository authority

`Docs/researches/math_theorems.md:6047-6052` supplies exactly the Chinese title "Kruskal algorithm,"
Joseph Kruskal, 1956, the gloss "a greedy algorithm for a minimum spanning tree," high importance,
and status `已验证` ("verified"). All six uncited lines originate at commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no formula, bibliography, graph or
algorithm definition, hypotheses, conclusion, proof boundary, correction history, or formal artifact.

`Docs/Stage0_Blueprint.md:22469-22494` repeats the gloss and explicitly leaves the formal system,
precise definitions and premises, proof route, dependencies, equivalent formulations, axioms,
machine state, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Primary-source lead

Joseph B. Kruskal Jr., *On the shortest spanning subtree of a graph and the traveling salesman
problem*, *Proceedings of the American Mathematical Society* 7(1) (1956), pages 48-50, DOI
`10.1090/S0002-9939-1956-0078686-7`, is the close source lead. Crossref metadata confirms the
author, title, venue, issue, date, pages, and DOI. A separately inspected official-paper discovery
copy has SHA-256 `b77f9dc058b996b0f78bb90b0f6af733338df63839d4d2e81ab194fa36870bd5`.

On page 48 the paper considers a finite connected graph with positive real edge lengths, initially
assumed distinct, and states that the shortest spanning tree is unique. Pages 48-49 give Problem 1
and Construction A: repeatedly select a shortest edge not previously selected and not forming a
loop; the resulting selected edges form a shortest spanning tree. Page 50 gives the exchange-style
proof using the first chosen edge missing from a competing tree and the unique cycle created by
adding it.

This is a primary-source discovery lead, not H0. The catalog does not cite it or choose between its
uniqueness and construction-correctness results. The received algorithm-family gloss remains H5
until an exact truth-valued proposition is approved. The edition has not been admitted as immutable repository
evidence; every incorporated definition and premise, the tie generalization, correction and errata
history, exact proof boundary, and an independent source-to-target review remain open.

## Literal crosswalk

| Repository phrase | Candidate source component | Prospective Lean component | Intake status |
|---|---|---|---|
| `Kruskal算法` | 1956 Construction A | executable or relational edge-selection procedure | candidate identity; not frozen |
| `贪心` | repeatedly choose a shortest admissible unchosen edge | ordered edge enumeration or minimum selection plus state transition | tie and determinism policy open |
| `不形成回路` | accept an edge only if no loop is created | `SimpleGraph.IsAcyclic` invariant and an edge-addition predicate | adjacent API probed; exact invariant open |
| `生成树` | final selected edges span the connected graph and form a tree | subgraph/spanning-coercion representation plus `IsTree` or `IsSpanning` | representation and boundary cases open |
| `最小` | no spanning tree has smaller total length | finite edge-weight sum and minimization over all spanning trees | weights and objective open |
| 1956/distinct lengths | positive real, pairwise-distinct edge lengths in the source lead | weight hypotheses and possible uniqueness conclusion | catalog does not select these premises |
| `已验证` | untrusted inventory label | human proof and kernel receipts would be required | no H0 or M credit |

## Neighbor and duplicate boundary

`THM-M-0824` is Prim's algorithm and cannot supply this root. Stage0 separately records
`THM-C-0094` with the more explicit gloss "Kruskal minimum spanning tree algorithm is correct."
That record is not a rev-5.6 target and is not owned by this dossier. It is useful only as duplicate-
boundary provenance; importing its stronger wording would broaden the authoritative catalog record.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`SimpleGraph.IsAcyclic`, `SimpleGraph.IsTree`, `SimpleGraph.Subgraph.IsSpanning`, subgraph edge sets,
spanning coercion, and the existence of a tree below a connected graph. The latter is unweighted
existence, not greedy optimality. A bounded exact-topic search found only the unrelated
Kruskal-Katona theorem and no minimum-spanning-tree algorithm or correctness declaration. No
canonical target, expression fingerprint, proof body, trust result, or machine-proof credit follows.

## Source gate

Before H0 or statement acceptance, accountable reviewers must preserve a lawful immutable source
edition; select one exact proposition and every incorporated definition; reconcile the catalog with
the source's finiteness, connectedness, positivity, distinct-weight, tie, and output conventions;
map the complete proof and assumptions; inspect corrections and errata; resolve every boundary case;
and independently approve the source-to-Lean crosswalk. Until then the canonical statement and
elaborated expression remain null.
