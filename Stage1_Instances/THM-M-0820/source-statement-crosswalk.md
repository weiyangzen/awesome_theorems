# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6026-6031` supplies exactly the title `Mirsky定理`, attribution
`Leon Mirsky`, year `1971`, gloss `偏序集分解为反链的最小数目`, importance `高`, and status
`已验证`. All six uncited lines originate in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`; their newline-preserving SHA-256 is
`07277e098e590c9d06714423d72d02e8ea6a226a1e59b763a2946cdfe7745dd3`.

`Docs/Stage0_Blueprint.md:22388-22413` repeats the gloss while explicitly leaving precise
definitions and premises, proof route, equivalent forms, axioms, machine state, and artifact links
open. The rev-5.6 manifest preserves `已验证` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Primary bibliographic lead

Crossref metadata for DOI `10.1080/00029890.1971.11992886` (alias `10.2307/2316481`) identifies:

> L. Mirsky, "A Dual of Dilworth's Decomposition Theorem," *The American Mathematical Monthly*
> 78(8), October 1971, pages 876-877.

The metadata records the title, author, journal, volume, issue, date, pages, and five references.
The publisher and JSTOR full-text links were not usable in this run, so the article text was not
inspected.
Consequently the exact theorem sentence, assumptions, definitions, proof, corrections, errata, and
independent review remain open. Bibliographic identity plus the repository gloss supports `H1`
discovery, not `H0`.

## Inspected theorem-family source

Abhishek Kr Singh, *Formalization of some central theorems in combinatorics of finite sets*,
arXiv:`1703.10977v1` (31 March 2017), was inspected from its 19-page PDF. The PDF SHA-256 is
`929c77c123421d5bade2ccfc4e40085afe827f558bf8661d16977c9581c46d8a`; the arXiv API response
SHA-256 is `4bb95b176fe2a8a5df03645062bb886e66930d3b037479d0d9cc7dec3c408cd0`.

The abstract and Section 4.1, printed pages 7-8, state that in a finite poset the size of a smallest
antichain cover equals the size of a largest chain. The printed Coq target is
`Theorem Dual_Dilworth: forall (P : FPO U), Dual_Dilworth_statement P`, where the latter quantifies
over natural numbers `m n`, an `Is_height P m` witness, and a smallest antichain cover of cardinality
`n`, and concludes `m = n`. Printed pages 3-4 make the carrier finite and inhabited. Appendix pages
18-19 define chains and antichains as inhabited subsets and an antichain cover as a family of
antichains whose union covers the carrier; pairwise disjointness is not required.

This is an inspected secondary exposition and Coq formalization that precisely discriminates the
theorem family and cites Mirsky's original as reference [17]. It is not the uninspected primary
paper, Lean evidence, an H0 source review, or permission to replace cover by partition without a
checked disjointization.

## Statement-component crosswalk

| Repository/source-family component | Required mathematical resolution | Pinned Lean candidate | Intake status |
|---|---|---|---|
| partially ordered set | finite type or finite subset; `PartialOrder`; nonempty policy | standard order structures | family fixed; carrier encoding open |
| chain maximum | maximum chain cardinality or height, including step/cardinality convention | `Set.chainHeight`, `LTSeries` | adjacent interface elaborates; convention open |
| antichain | pairwise incomparable subset under `<=` | `IsAntichain (· <= ·)` | definition elaborates |
| decomposition | source-matched antichain cover; optional exact partition only after checked disjointization | indexed family or `Finpartition (Finset.univ)` | representation and transport open |
| minimum number | minimum over admissible covers, or a checked-equivalent partition witness plus lower bound | finite-cardinality/order APIs | no canonical expression selected |
| equality with height | minimum antichain-part count equals maximum chain cardinality | no target-specific declaration located | proof and transport open |

## Pinned Lean discovery boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `Mathlib.Order.Antichain` defines `IsAntichain` and proves basic closure and chain-intersection
  facts;
- `Mathlib.Order.Height` defines `Set.chainHeight` and provides finite maximum-chain witnesses;
- `Mathlib.Order.Partition.Finpartition` supplies finite exact partitions and part-cardinality APIs;
  and
- `Mathlib.Order.RelSeries` supplies strict chains and finite-dimensional longest-series APIs.

`IntakeProbe.lean` checks representative declarations using the pinned toolchain. A bounded search
over repository Lean sources and pinned mathlib found no lexical `Mirsky` declaration and no
target-specific antichain-partition/minimum-chain-height bridge. Absence from this bounded search is
not an exhaustive anchor-audit result. No canonical target, checked height-convention transport,
terminal body, transitive provenance, placeholder/axiom closure, wrapper, or M0 credit is claimed.

## Admission gate

Before `H0`, an independent source reviewer must inspect a lawful immutable copy of the article,
pinpoint the theorem and incorporated definitions, map every premise and conclusion, record
correction/errata status, and approve the source-to-Lean crosswalk. Before statement acceptance,
the integration lane must separately approve the exact Lean expression, height and partition
encodings, fingerprints, transports, and mutation suite.
