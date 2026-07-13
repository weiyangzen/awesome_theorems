# Source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:6320-6325` contains:

- title: `Menger定理` (Menger's theorem);
- proposer: Karl Menger;
- time: 1927;
- statement gloss: `顶点连通度与不相交路径` (vertex connectivity and disjoint paths);
- importance: high; and
- formalization status: `已验证` (verified).

Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no proposition, graph class,
terminals, disjointness predicate, separator, parameter `k`, finiteness premise, conclusion, proof
boundary, errata, reviewer, or formal artifact. The verified label is untrusted metadata under
rev-5.6.

## Literal crosswalk

| Repository phrase | Material ambiguity | Required exact source component | Intake status |
|---|---|---|---|
| `顶点连通度` / vertex connectivity | predicate `k`-connected versus numeric connectivity; local versus global | exact definition, graph-order premise, and quantified `k` | open |
| `不相交路径` / disjoint paths | vertex-disjoint versus internally vertex-disjoint; endpoints/terminal sets | path family and exact pairwise predicate | open |
| `与` / and | equality, equivalence, characterization, or informal relation | exact logical connective and conclusion orientation | open |
| Karl Menger / 1927 | attribution without a work locator | edition, passage, definitions, assumptions, proof, errata | source identity located; mapping open |
| `已验证` | inventory label only | no human or machine proof component | explicitly untrusted |

The rows do not determine a canonical claim, so `instance.json` leaves both the human statement
and Lean expression null.

## Primary-source identity

DOI `10.4064/fm-10-1-96-115` identifies Karl Menger, *Zur allgemeinen Kurventheorie*,
*Fundamenta Mathematicae* 10 (1927), pages 96-115. The publisher supplied a 10-page scan observed
on 2026-07-13 with SHA-256
`45f0dce723f85dae5d360892b6e9596aeaef70ea222b3ea9a0ea2e7c54ae3602`. The DOI metadata
response had SHA-256 `5d801900763f0e3e77c229ecd27792c7170866b8035d6451ce8176a90b8b85cf`
and independently confirms the author, title, journal, volume, pages, year, and DOI.

The scan is image-only. Visual inspection located `Satz beta`, beginning on printed page 100 and
closing on page 102. Its theorem sentence reads:

> Ist K ein kompakter regulaerer eindimensionaler Raum, welcher zwischen den beiden endlichen
> Mengen P und Q n-punktig zusammenhaengend ist, dann enthaelt K n paarweise fremde Boegen, von denen
> jeder einen Punkt von P und einen Punkt von Q verbindet.

This ASCII transcription transliterates `Satz beta` and the scan's German diacritics. A
conservative, not independently reviewed translation is: if `K` is a compact regular
one-dimensional space that is `n`-point connected between the finite sets `P,Q`, then `K` contains
`n` pairwise disjoint arcs, each joining a point of `P` to one of `Q`. The preceding definition uses
the nonexistence of a separating set with fewer than `n` points. The result is topological, not
literally a finite-simple-graph global vertex-connectivity theorem. Definition-chain transcription,
proof mapping, terminology and translation review, graph transport, corrections, and errata remain
open. It strengthens the primary family locator but is not an exact E4 crosswalk or H0 for the
catalog target.

## Inspected modern source lead

Reinhard Diestel, *Graph Theory*, sixth edition (2025), author-hosted Chapters 1 and 3, provides a
pinpoint modern family source:

- Theorem 3.3.1, printed page 71: for a finite graph and vertex sets `A,B`, the minimum number of
  vertices separating `A` from `B` equals the maximum number of disjoint `A`-`B` paths;
- Corollary 3.3.5(i), printed page 75: for distinct nonadjacent vertices, the minimum separating
  vertex count equals the maximum number of independent paths;
- Theorem 3.3.6(i), printed page 76: a graph is `k`-connected exactly when it contains `k`
  independent paths between every two vertices; and
- the chapter notes, printed page 91: the global version was first stated and proved by Whitney in
  1932, while Menger's theorem goes back to the 1927 paper.

Chapter 1 uses simple undirected graphs and defaults to finite graphs here, defines independent
paths by shared inner vertices, defines separation of terminal sets, and includes `|G| > k` in
`k`-connectivity. The observed Chapter 3 PDF/text SHA-256 values are respectively
`1d54f8cf0a846e8acedc5a5eb87839173a3145148a6c23eba49e4d4d6d0c8775` and
`32d3e2e70d912de714c2ec2529835627437be4a7b44382a2c529992a6baa0268`; Chapter 1 PDF/text
values are `ebd9084653a1a534b964cbe327eeb8ab6b46a5e98deeee94280b05ebb6f37b56` and
`94ff5b77d20b0499aed7aa377d9aa223f0fa610f68c67d7d21e1850790f6b6f7`.

This source shows that the catalog gloss and attribution do not identify one root. The catalog does
not cite Diestel, choose the core theorem over the global result, or resolve the Whitney attribution
boundary. Complete definition/proof mapping, correction status, catalog-to-source selection, and
independent review remain open. The truthful human-source level is `H1`.

## Overlapping-record crosswalk

`Docs/researches/math_theorems.md:5977-5982` separately records `门格尔定理`, Karl Menger, 1927,
with the gloss `图中不相交路径的最大数目`, projected as `THM-M-0813`. The two records share an
eponym, attribution, year, importance, and untrusted status, but differ in title spelling and gloss.
The generator therefore kept both records. No accepted source identity, alias, deduplication, or
root-ownership decision exists. The overlap is a scope blocker, not evidence for either target.

## Lean crosswalk

The pinned probe elaborates adjacent interfaces:

| Lean interface | What it authenticates | Missing Menger component |
|---|---|---|
| `SimpleGraph.Path` | a walk with no repeated vertices | no family packing or connectivity characterization |
| `SimpleGraph.Reachable` | existence of a walk between two vertices | no disjoint family or separator relation |
| `SimpleGraph.Reachable.exists_isPath` | reachable vertices admit a path | only one path |
| `SimpleGraph.induce` | restriction to a vertex subtype | no selected deletion/separator convention |
| `SimpleGraph.IsEdgeReachable` | reachability after small edge deletion | edge, not vertex, connectivity infrastructure |
| `SimpleGraph.IsEdgeConnected` | pairwise edge reachability | no vertex-disjoint path characterization |
| `SimpleGraph.Walk.IsPath.disjoint_support_of_append` | support disjointness inside one path append | not pairwise independent paths |

The bounded exact-topic search located no direct Menger declaration, vertex-connectivity
definition, or vertex-separator/path-packing theorem. These are encoding ingredients only, so
machine debt remains `M4`.

## Gate result

The intake freezes `[H1, M4, R4]`. A statement-phase retry needs an accepted identity and ownership
decision for `THM-M-0862` versus `THM-M-0813` and an independently reviewed exact source
proposition fixing every scope row. Only then may that same proposition be elaborated with minimal
imports, expression and environment fingerprints, checked transports, and all required mutations.
