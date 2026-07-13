# Source-statement crosswalk

## Repository record

The source inventory at `Docs/researches/math_theorems.md:5977-5982` contains exactly:

- title: `门格尔定理` (Menger's theorem);
- proposer: Karl Menger;
- time: 1927;
- statement gloss: `图中不相交路径的最大数目` (the maximum number of disjoint paths in a graph);
- importance: high; and
- formalization status: `已验证` (verified).

Git history places all six uncited lines in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. They contain no proposition, equality, graph class,
terminal data, disjointness convention, separator, finiteness premise, conclusion, proof boundary,
errata, reviewer, or formal artifact. Under rev-5.6 the verified label is untrusted metadata.

## Literal crosswalk

| Repository phrase | Material ambiguity | Required exact source component | Intake status |
|---|---|---|---|
| `图中` / in a graph | finite/infinite, simple/multi, directed/undirected | graph model, carrier, finiteness, typeclasses | open |
| `路径` / paths | endpoints or endpoint sets; trivial paths | path definition, terminal membership, length convention | open |
| `不相交` / disjoint | vertex, internal-vertex, or edge disjointness | family representation and exact pairwise predicate | open |
| `最大数目` / maximum number | no comparator or equality is stated | separator/cut quantity and equality/equivalence orientation | open |
| Karl Menger / 1927 | attribution without a work locator | edition, theorem/page, definitions, assumptions, proof, errata | source identified; mapping open |
| `已验证` | inventory label only | no human or machine proof component | explicitly untrusted |

The rows do not determine one canonical claim, so `instance.json` leaves both the human statement
and Lean expression null.

## Primary-source identity

The DOI `10.4064/fm-10-1-96-115` identifies Karl Menger, *Zur allgemeinen Kurventheorie*,
*Fundamenta Mathematicae* 10 (1927), pages 96-115. The publisher supplied a 10-page scan observed
on 2026-07-13 with SHA-256
`45f0dce723f85dae5d360892b6e9596aeaef70ea222b3ea9a0ea2e7c54ae3602`. The DOI metadata response
and publisher page independently identify the author, title, journal, volume, pages, year, and DOI.

The scan is image-only and its title concerns general curve theory. This intake did not transcribe
the German text, locate the exact graph-theoretic theorem within it, map its topological notions to
finite graph paths and separators, audit corrections or translations, or obtain independent review.
It therefore provides immutable primary-source identity and a future audit input, not an exact E4
crosswalk or H0.

## Inspected modern source lead

Reinhard Diestel, *Graph Theory*, sixth edition (2025), author-hosted Chapter 3, Section 3.3,
Theorem 3.3.1 (printed page 71), states:

> Let `G = (V,E)` be a graph and `A,B` subsets of `V`. The minimum number of vertices separating
> `A` from `B` in `G` equals the maximum number of disjoint `A`-`B` paths in `G`.

The author-hosted Chapter 1 defines finite graphs, paths, separation of terminal sets, and
`k`-connectivity. Section 3.3 then separately states Corollary 3.3.5 for nonadjacent vertices and
edge-disjoint paths, and Theorem 3.3.6 for global vertex and edge connectivity. The observed Chapter
3 PDF had SHA-256 `1d54f8cf0a846e8acedc5a5eb87839173a3145148a6c23eba49e4d4d6d0c8775`.

This source is sufficiently precise to demonstrate why the catalog gloss is ambiguous, but the
catalog does not cite this edition or select Theorem 3.3.1 rather than one of its corollaries. The
definition chain, proof, edition corrections, source-to-catalog choice, and independent review are
not accepted. The truthful human-source level is `H1`.

## Duplicate-record crosswalk

`Docs/researches/math_theorems.md:6320-6325` separately records `Menger定理`, Karl Menger, 1927,
with the gloss `顶点连通度与不相交路径` (vertex connectivity and disjoint paths), projected as
`THM-M-0862`. The two records share eponym, attribution, year, importance, and untrusted status, but
their glosses differ. No accepted source identity, alias, deduplication, or theorem-root ownership
decision exists. The duplicate is a scope blocker, not evidence that `THM-M-0813` means the global
vertex-connectivity form.

## Lean crosswalk

The pinned probe elaborates the following adjacent interfaces:

| Lean interface | What it authenticates | Missing Menger component |
|---|---|---|
| `SimpleGraph.Path` | a walk with no repeated vertices | no family packing or extremal count |
| `SimpleGraph.Reachable` | existence of a walk between two vertices | no disjoint family or separator equality |
| `SimpleGraph.Reachable.exists_isPath` | reachable vertices admit a path | only one path |
| `SimpleGraph.induce` | restriction to a vertex subtype | no selected deletion/separator convention |
| `SimpleGraph.IsEdgeReachable` | reachability after fewer than `k` deleted edges | edge-connectivity definition, not path packing equivalence |
| `SimpleGraph.IsEdgeConnected` | pairwise `k`-edge-reachability | no disjoint-path characterization |
| `SimpleGraph.Walk.IsPath.disjoint_support_of_append` | local disjoint support inside one appended path | not pairwise disjoint independent paths |

The exact-topic search located no direct Menger declaration, vertex-connectivity definition, or
vertex-separator/path-packing theorem. These are useful definitions, not a formal candidate for the
missing root, so machine debt remains `M4`.

## Gate result

The intake freezes `[H1, M4, R4]`. A statement-phase retry requires an accepted identity/ownership
decision for `THM-M-0813` and `THM-M-0862`, plus an independently reviewed exact source proposition
that fixes every scope row. Only then may the same proposition be elaborated with minimal imports,
expression and environment fingerprints, checked alternate transports, and all required mutations.
