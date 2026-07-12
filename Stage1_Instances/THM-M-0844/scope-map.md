# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0844`, the eponym `Alon-Fischer-Newman定理`, attribution to
Alon, Fischer, and Newman, the year 2007, and the gloss `正则性引理的测试` (literally "testing of the
regularity lemma"). Intake preserves the graph-theory/property-testing/regularity subject boundary
without turning this noun phrase into a theorem or guessing what "testing" quantifies over.

## Candidate families not credited

These discovery hypotheses are mathematically distinct and none is selected at intake:

1. A bounded-VC-dimension, ultra-strong regularity lemma for finite bipartite graphs: a partition
   with polynomially many parts and almost all cross-pairs nearly complete or nearly empty.
2. A property-testing theorem for bipartite graphs excluding specified induced subgraphs, including
   an algorithmic query-complexity conclusion.
3. A characterization of testable dense-graph properties through regular partitions, as in the
   four-author Alon-Fischer-Newman-Shapira work.
4. The Fischer-Newman theorem that every testable dense-graph property is estimable.
5. Szemeredi's ordinary regularity lemma, which the repository separately owns as `THM-M-0843`.

The 2007 three-author paper is the leading identity candidate because its authors and year match
exactly. Later sources attribute a polynomial bounded-VC regularity result to it, but that does not
establish which numbered theorem the catalog intended or whether the catalog instead meant its
testing result.

## Proposition-changing decisions

Before statement elaboration, an approved source decision must freeze all of the following:

- the exact primary paper revision, incorporated definitions, theorem number, pages, proof boundary,
  corrections, and independent source review;
- whether the objects are finite bipartite graphs, ordinary simple graphs, hereditary properties,
  forbidden induced bigraphs, adjacency matrices, or set systems;
- finite vertex types and bipartition conventions, or the source's two-sorted matrix convention;
- the source's VC-dimension or dual-VC-dimension definition, including which neighborhood family is
  measured and the treatment of repeated/equal rows and empty sides;
- edit-distance normalization, one-sided versus two-sided testing, success probability, tester
  adaptivity, query model, and whether an algorithmic result is part of the conclusion;
- the regularity notion: epsilon-homogeneous versus epsilon-regular/uniform pairs, equitable or
  arbitrary partitions, exceptional pairs or vertices, and all density thresholds;
- the ordered dependence among dimension, error, forbidden family, graph size, part bound, query
  bound, and hidden or explicit constants;
- exact quantifier order, strict versus non-strict inequalities, rounding, positivity and
  nonemptiness assumptions, and every degenerate case; and
- whether the conclusion is existence, efficient construction, testability, characterization, or a
  conjunction, with no result imported merely because it is used in the proof.

These choices change the proposition. A familiar bounded-VC regularity statement cannot be selected
from a later paraphrase and called the catalog theorem without checking the primary result.

## Explicit exclusions

- The ordinary Szemeredi regularity lemma or its pinned mathlib declaration as a replacement.
- A theorem from the four-author characterization paper with Shapira omitted.
- The two-author Fischer-Newman testing-versus-estimation theorem with Alon added.
- A VC-dimension lemma, graph partition definition, or induced-subgraph API by itself.
- A predicate or structure that assumes the desired partition or tester and then projects it.
- A randomized experiment, sampled adjacency matrix, asymptotic heuristic, or unverified algorithm.
- The catalog label `已验证` as human-source or Lean kernel evidence.

## Boundary cases

The statement phase must resolve empty and singleton vertex sides, zero VC-dimension, zero or large
error, forbidden families containing trivial matrices/graphs, empty properties, diagonal and loop
conventions, induced versus non-induced containment, ordered versus unordered bipartitions,
exceptional parts, rounding of part sizes, small graphs below asymptotic thresholds, randomized
failure probability, and whether complexity bounds are existential or algorithmic.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks finite set-family
VC-dimension, bipartite simple graphs, graph density and uniformity, partitions, and the ordinary
Szemeredi regularity theorem. A bounded source search found no Alon-Fischer-Newman or graph property
testing declaration. These are intake feasibility observations, not an exhaustive anchor audit or
proof evidence.
