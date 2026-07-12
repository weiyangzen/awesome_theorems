# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6194-6199` supplies exactly the title
`Alon-Fischer-Newman定理`, authors Alon/Fischer/Newman, year 2007, the gloss
`正则性引理的测试`, importance "high," and status `已验证`. Git history attributes all six uncited
lines to repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no
bibliography, stable source ID, theorem/page locator, definition, binder, hypothesis, conclusion,
proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:23036-23061` repeats the gloss while explicitly leaving exact definitions
and premises, proof process, dependencies, alternate forms, axioms, machine status, and artifact
links open. Its generic planning language about a known closed result is not source evidence. The
rev-5.6 manifest preserves `已验证` only in `source_status_untrusted` and resets this target to
`L0 / rework_required`.

## Literal crosswalk

| Catalog element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| Alon-Fischer-Newman | one exact jointly authored result | one source-matched `Prop` | eponym is not a source locator |
| 2007 | publication/revision discriminator | immutable source revision metadata | matches one strong candidate only |
| "regularity lemma" | exact partition, density, error, and complexity definitions | `Finpartition`, graph density/uniformity, or source-specific alternatives | version and conclusion absent |
| "testing" | algorithm/property-testing contract or a claim about testing regularity | quantified tester, distance, probability, and query complexity | object and meaning absent |
| `已验证` | untrusted inventory field | source proof and kernel receipt would be required | no H or M credit |

The gloss is a noun phrase rather than a quantified assertion. It does not say whether a regularity
lemma enables a tester, is itself algorithmically tested, or is a structural characterization of
testability.

## Leading bibliographic candidate

Crossref and DBLP identify the exact three-author 2007 article:

> Noga Alon, Eldar Fischer, and Ilan Newman, *Efficient Testing of Bipartite Graphs for Forbidden
> Induced Subgraphs*, SIAM Journal on Computing 37(3) (2007), 959-976,
> DOI `10.1137/050627915`.

The metadata match is strong but remains discovery evidence. Crossref supplies the bibliographic
record, not the theorem text. Unpaywall reported the article closed and no repository copy; the
author-copy URL returned by Semantic Scholar was unavailable during this bounded intake. No theorem
number, exact statement, proof, or errata was inspected, so the article is not admitted to H0.

Fox, Pach, and Suk, *Erdos-Hajnal conjecture for graphs with bounded VC-dimension*, arXiv
`1710.03745v1`, explicitly cites this article as reference [2]. Its pages 3-4 say Alon, Fischer, and
Newman proved for bipartite graphs of VC-dimension `d` an ultra-strong regularity result whose
number of parts can be `(d/epsilon)^{O(d)}`; the surrounding definition uses equitable partitions
with all but an epsilon-fraction of pairs epsilon-homogeneous. This is a valuable source-family
discriminator, not a verbatim replacement for the primary theorem: it suppresses exact constants,
thresholds, quantifier order, definitions, and possibly algorithmic clauses.

## Confusable results explicitly not selected

1. Noga Alon, Eldar Fischer, Ilan Newman, and Asaf Shapira, *A Combinatorial Characterization of
   the Testable Graph Properties: It's All About Regularity*, STOC 2006, DOI
   `10.1145/1132516.1132555`, later SIAM Journal on Computing 39(1) (2009), DOI
   `10.1137/060667177`. Its title fits the gloss closely, but its fourth author and dates conflict
   with the catalog metadata.
2. Eldar Fischer and Ilan Newman, *Testing versus estimation of graph properties*, SIAM Journal on
   Computing 37 (2007), 482-501. Later literature calls its result the Fischer-Newman theorem:
   every testable dense-graph property is estimable. It has no Alon and is a different conclusion.
3. Szemeredi's regularity lemma is independently cataloged as `THM-M-0843` and appears in pinned
   mathlib as `szemeredi_regularity`. Neither its source nor its proof credit transfers here.

The repository may have compressed, mistranslated, or conflated these topics. Intake records that
risk rather than choosing the most convenient theorem.

## Source gate

There is no repository-selected mathematical proposition. Before leaving `H5`, an accountable
reviewer must identify and lawfully preserve the intended primary source, inspect the exact numbered
result and incorporated definitions, map every binder/hypothesis/conclusion and proof boundary,
audit corrections and errata, distinguish structural from algorithmic clauses, reconcile the
confusable papers, and obtain independent approval. Only then may the statement phase freeze and
mutation-test an identical Lean expression.

`H5` here does not assert that the cited papers or their regularity results are false. It records
that the catalog phrase is not yet a truth-valued target a Lean kernel could check.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery-only probe
checks `Finset.Shatters`, `Finset.vcDim`, `SimpleGraph.IsBipartite`,
`SimpleGraph.IsUniform`, `Finpartition.IsUniform`, `Finpartition`, and
`szemeredi_regularity`. These are relevant substrate, not an AFN statement or proof. A bounded
case-insensitive search for the authors, forbidden-induced testing, and graph-property testing over
pinned mathlib and repo-local Lean sources found no exact-topic declaration. The later immutable
formal-candidate audit remains open.

The canonical module, declaration or expression, expression and environment fingerprints, checked
alternate encodings, and statement mutations therefore remain null. No formal absence theorem,
statement elaboration, proof, audit completion, or theorem completion is claimed.
