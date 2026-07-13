# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6397-6402` supplies exactly the title `图的同构问题`, collective
attribution, twentieth-century date, gloss `图同构的复杂性`, importance "high," and status
`准多项式时间解决`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

The record contains no bibliography, graph or input encoding, machine or cost model, ordered
binders, hypotheses, exact bound, proof boundary, correction history, reviewer, or formal artifact.
Stage0 repeats these omissions. The manifest preserves the status only as untrusted metadata and
resets the target to `L0 / rework_required`.

## Inspected result and correction sources

László Babai, *Graph Isomorphism in Quasipolynomial Time*, arXiv `1512.03547v2`, 19 January
2016, was inspected in an 89-page PDF (843,393 bytes; SHA-256
`b6393ff36f4ff1c9646d7b9c5ea9ef78cfb222d52634ffdef2f05fa77daa9c62`). Page 4 defines a
function as quasipolynomially bounded when some constants `c`, `C` give
`f(n) <= exp(C (log n)^c)` for all sufficiently large `n`. Theorem 1.1.1 gives the String
Isomorphism result; Corollary 1.1.2 states that Graph Isomorphism and Coset Intersection can be
solved in quasipolynomial time. The surrounding text maps an `n`-vertex graph to a binary string
indexed by unordered vertex pairs.

The arXiv API still identifies version 2 as the latest revision of `1512.03547`; there is no
post-January-2017 corrected revision under that identifier. Version 2 is therefore never labeled a
corrected proof in this dossier and must be read only with the later correction evidence.

Harald A. Helfgott, with an appendix by Jitendra Bajpai and Daniele Dona, *Graph isomorphisms in
quasi-polynomial time*, arXiv `1710.04574v1`, 12 October 2017, was inspected in a 67-page PDF
(659,668 bytes; SHA-256
`f16a953a084a4bc4b77e30b5d0fb35557a566d5d869bf42de155400466b9f2d2`). At printed page
1125-02 (PDF page 2), it defines finite graph isomorphism and the directed/undirected
graph-to-string reduction, states in Theorem 1.1 that String Isomorphism is solvable in
quasi-polynomial time in the domain size, and states in Corollary 1.2 that Graph Isomorphism is
solvable in quasi-polynomial time in the number of vertices. Helfgott says preparation of the
exposition exposed a nontrivial timing-analysis error, Babai repaired it by simplifying the
algorithm, and the proof is now correct. The exposition explicitly aims to examine the proof in
detail to remove doubt about the repaired result. Its footnote 17 at printed page 1125-31 locates
the original failure at the corrected Bipartite Split-or-Johnson branch and explains why the prior
forked reduction caused catastrophic index growth. Printed page 1125-38 derives an
`exp((log n)^c)` bound for `n`-vertex Graph Isomorphism and notes that the detailed analysis gives
`c = 3`.

Babai's author update, *Graph Isomorphism update, January 9, 2017* (retrieved HTML: 4,776 bytes;
SHA-256 `d96a4083ffd3b0b6931500f13e81a33ecb3ec5ab9eebadb64c2fca476faf42ca`), records that the
quasipolynomial claim was withdrawn on 4 January after Helfgott found the timing error, restored on
9 January after a replacement recursive call, and accompanied by a fix on 14 January. The linked
four-page CC-BY note, *Fixing the UPCC case of Split-or-Johnson* (168,694 bytes; SHA-256
`e4438bf10d131f4642bee9aa29dfbd9fc133776705c85c3fe3d466da38b95653`), identifies the bad
recursive call and its replacement. It also records a separate Design Lemma error found by Jin-Yi
Cai and review of the modified analysis by Gabor Tardos and Helfgott.

The author's later version 2.5, dated 2 November 2018 (109 pages; 873,346 bytes; SHA-256
`3b80cf8a602311a28beac4ae235bc2fbdc89301cd2075671359c2171c444ea9c`), repeats the headline
result and records both fixes, but warns that the revision is incomplete and retains notational,
conceptual, and organizational inconsistencies. It is correction-history evidence, not the sole
source of the post-fix claim. It was observed at
`http://people.cs.uchicago.edu/~laci/quasi25.pdf`; the author host's HTTPS certificate did not
verify in this environment, so the transport itself is not release-grade evidence.

Crossref identifies the 2016 STOC extended abstract as DOI `10.1145/2897518.2897542`, pages
684-697. The publisher text was not obtained or compared. The observed materials are digest-bound
discovery inputs, not vendored source artifacts, a Stage1-accepted edition/correction bundle,
complete source-to-node mapping, an independent dossier review receipt, or H0 evidence.
The scoped offline checker verifies the recorded digest fields and dossier consistency; it does not
possess or reacquire the external bytes and therefore does not independently recompute their
digests.

## Clause crosswalk

| Catalog/source element | Necessary mathematical component | Prospective Lean component | Intake status |
|---|---|---|---|
| graph isomorphism | decision predicate for pairs of finite graphs | serialization plus checked `Nonempty (G ≃g H)` correspondence | representation and encoding open |
| "complexity" | deterministic machine and worst-case cost semantics | resource-bounded language/algorithm framework | no exact framework selected |
| "quasipolynomial" | eventual `exp(C (log n)^c)` bound | quantified constants, threshold, runtime inequality | binders and numeric conventions open |
| "can be solved" | total correct decision algorithm with the bound | procedure, correctness, termination, cost certificate | no canonical expression |
| catalog status | source-specific closed branch | independently accepted evidence state | untrusted metadata only |

The catalog wording and source family do not assert polynomial time, NP-intermediacy, or
NP-completeness consequences. Corollary 1.1.2 also does not by itself choose a Lean representation
or prove a transport from the source's informal encoding.

## Source gate

The provisional source classification is `H1`: a published, author-authored theorem family and
pinpoint statements are identified, but exact edition selection, incorporated definitions,
assumption and binder mapping, final correction/errata disposition, proof-node crosswalk,
publisher-version comparison, and independent review remain open. Before H0 or statement closure,
an accountable reviewer must resolve each item and the ownership relationship with `THM-M-0874`
and duplicate `THM-M-1567`.

## Lean discovery boundary

Pinned mathlib supplies `SimpleGraph.Iso` (`G ≃g H`) as adjacency-preserving equivalence,
`Language` as sets of words, and `ManyOneReducible`/`OneOneReducible` as computable reductions.
The probe re-elaborates these interfaces. It supplies no resource-bounded machine model,
quasipolynomial class, graph-isomorphism language, algorithm, source transport, or proof body.

The canonical module, target expression, expression and environment fingerprints, alternate
encodings, and statement mutations remain null. No exact formal statement, formal absence theorem,
branch proof, audit completion, or theorem completion is claimed.
