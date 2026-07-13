# THM-M-0825 source-statement crosswalk

## Repository source and provenance

The complete mathematics-catalog record is `Docs/researches/math_theorems.md:6061-6066`:

| Field | Literal value | Intake meaning |
|---|---|---|
| title | `Dijkstra算法` | names the Dijkstra algorithm family |
| proposer | `Edsger Dijkstra` | historical attribution |
| time | `1959` | primary-source-family locator |
| statement | `单源最短路径算法` | method/purpose gloss, not a truth-valued proposition |
| importance | `高` | scheduling metadata only |
| formalization status | `已验证` | explicitly untrusted; no H/M credit |

All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no bibliography, formula,
definitions, ordered binders, hypotheses, conclusion, proof locator, correction record, reviewer,
or formal artifact. `Docs/Stage0_Blueprint.md:22523-22548` repeats the gloss while expressly leaving
the exact definitions and premises, proof route, dependencies, equivalent forms, axioms, machine
status, and artifact links open.

The separate record `THM-C-0091` in `Docs/researches/cs_theorems.md:166` says only that Dijkstra's
algorithm correctly finds shortest paths. It is a different UID outside the rev-5.6 M-target set
and is itself binder-incomplete. It is neighbor provenance, not authority or proof for this target.

## Inspected primary-source lead, not H0

E. W. Dijkstra, "A Note on Two Problems in Connexion with Graphs," *Numerische Mathematik* 1,
pages 269-271 (1959), DOI `10.1007/BF01386390`.

A three-page scan served by Yale's reading archive was inspected on 2026-07-13. Its SHA-256 is
`baa66780e853ef06e8bf9c0d8c37e2e0a652e9f5252811e97fb2848d0514fba5`; the scan was not
added to the repository. Springer article metadata and Crossref independently confirm the author,
title, journal, year, and page range.

- Page 269 fixes `n` nodes, some or all pairs connected by branches with given lengths, and at least
  one path between every pair. It first treats a minimum-total-length tree as Problem 1.
- Page 270 states Problem 2: find a path of minimum total length between two given nodes `P` and `Q`.
  It says minimum paths from `P` are constructed in increasing length until `Q` is reached, defines
  settled/frontier/remaining node and branch sets, then gives a relaxation step and a step selecting
  the frontier node with minimum tentative distance.
- Page 270 says the solution is found when `Q` enters the settled set and remarks that branch length
  may depend on traversal direction. Page 271 discusses storage and relative work informally; it
  does not state a modern asymptotic complexity theorem.

This is a strong pinpoint primary source, so the provisional human status is `H1`: a published
algorithm and intended correctness family are identifiable, but exact statement fidelity remains
unreviewed. The paper does not literally state the catalog's modern all-vertices single-source
output contract, formalize its proof invariant, or spell out a modern weight type and nonnegativity
predicate. No accepted immutable source packet, correction/errata audit, full definition and
premise crosswalk, proof-node mapping, or independent source review exists. Therefore it is not
`H0` evidence.

## Clause crosswalk

| Catalog/source element | Mathematical information fixed | Required Lean component | Intake result |
|---|---|---|---|
| `单源` / source `P` | paths grow outward from one distinguished node | source binder and reachability domain | family identified; all-vertex versus one-target output open |
| `最短路径` | page 270 minimizes total branch length | path/walk type, additive cost, minimum predicate, unreachable convention | representation and boundary open |
| `算法` | page-270 settled/frontier sets, relaxation, and minimum selection | executable function or transition relation plus termination | no formal algorithm selected |
| correctness | page 270 says the solution has been found when `Q` is settled | exact invariant, output relation, partial/total correctness theorem | proof boundary not accepted |
| branch lengths | lengths are given; direction dependence is allowed by Remark 1 | weight type, edge mapping, order/addition laws, nonnegativity | codomain and hypotheses open |
| global paths | page 269 assumes a path between every pair | connectivity or reachability premise | conflict/transport to modern partial SSSP open |
| page-271 work comments | qualitative storage/work comparison | explicit cost model and asymptotic proposition | no complexity theorem fixed |
| `已验证` | repository screening label | source review or kernel receipt would be required | no credit |

The repository gloss has no ordered binders or conclusion whose truth Lean can check. Consequently
no canonical expression, alternate encoding, or expression hash can be populated truthfully at
intake.

## Pinned Lean substrate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Module/declarations | Actual role | Credit boundary |
|---|---|---|
| `Mathlib.Combinatorics.SimpleGraph.Metric`: `SimpleGraph.edist`, `edist_le`, `reachable_of_edist_ne_top` | unweighted undirected shortest-walk distance | semantic substrate; no Dijkstra algorithm |
| same module: `SimpleGraph.Reachable.exists_walk_length_eq_edist` | an unweighted shortest walk attains `edist` when reachable | existence/specification only |
| `Mathlib.Combinatorics.Quiver.Path.Weight`: `Quiver.Path.addWeight`, `addWeight_comp`, `addWeight_nonneg` | additive edge-weight accumulation and elementary laws | weighted-path substrate only |
| `Mathlib.Combinatorics.Quiver.Arborescence`: `Quiver.shortestPath`, `shortest_path_spec` | noncomputable edge-count-minimal path under rooted connectivity | not weighted Dijkstra correctness |

`IntakeProbe.lean` authenticates these exact interfaces. Bounded repository and pinned-mathlib
searches found no declaration named for Dijkstra and no implementation/correctness theorem. These
observations are intake discovery only, not the later immutable anchor audit, global absence proof,
or machine-proof credit.

## Source exit gate

Before statement execution, accountable source and graph-algorithm reviewers must approve a lawful
immutable edition and one exact theorem/proof boundary, incorporated definitions and corrections,
and a row-by-row mapping from the source/corrected target to every binder, premise, conclusion, and
boundary case. A Lean reviewer must then freeze minimal imports, exact expression and environment
fingerprints, checked transports, and the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. Until those gates pass, the truthful classification is
`[H1, M4, R4]`, and all proof, audit-completion, and theorem-completion claims remain open.
