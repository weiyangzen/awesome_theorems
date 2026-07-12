# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6488-6493` supplies the title
`Marcus-Spielman-Srivastava theorem`, the attribution `Marcus/Spielman/Srivastava`, the year 2015,
the gloss `existence of biregular Ramanujan graphs`, importance `high`, and status `verified`. Git
history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:24170-24194` repeats the gloss while leaving exact definitions and
premises, proof route, dependencies, equivalent forms, axiom policy, machine status, and artifact
links open. The rev-5.6 target manifest preserves `verified` only as untrusted metadata and resets
the target to `L0 / rework_required`.

The repository gives no bibliography, theorem/page locator, degree range, graph convention,
spectral definition, sequence distinctness condition, proof boundary, errata review, or reviewer.
It therefore identifies a result family but does not itself freeze one formal proposition.

## Exact primary candidate

Adam W. Marcus, Daniel A. Spielman, and Nikhil Srivastava, *Interlacing families I: Bipartite
Ramanujan graphs of all degrees*, *Annals of Mathematics* 182 (2015), no. 1, 307-325, DOI
`10.4007/annals.2015.182.1.7`. The official article page is
`https://annals.math.princeton.edu/2015/182-1/p07`, and its PDF is
`https://annals.math.princeton.edu/wp-content/uploads/annals-v182-n1-p07-p.pdf`.

The official published PDF was inspected. Its SHA-256 is
`1c0f058b4adaa37cfc6e0ce8d75ca67204e725a09fc124228ccbdaabb8ab60cf`. The immutable arXiv
`1304.4132v2` PDF was also inspected; its SHA-256 is
`4da468fe22413c0c8a9f77651711db4edadda7d34986e34673db2cd8192bddfb`.
The immutable record and PDF URLs are `https://arxiv.org/abs/1304.4132v2` and
`https://arxiv.org/pdf/1304.4132v2`.
The arXiv record was submitted in 2013 and revised in 2014; 2015 is the journal publication year
used by the catalog.

Published Theorem 5.6 begins on journal page 316 and its proof continues on page 317:
for all `c,d >= 3`, there exists an infinite sequence of `(c,d)`-biregular bipartite Ramanujan
graphs. This exactly matches the unusual word `biregular` in the catalog gloss and is therefore the
primary canonical candidate. It is not yet admitted as the canonical repository claim: a complete
definition/assumption/proof/errata crosswalk and independent review remain open.

The published sentence places "there exists" before "for all", while arXiv v2, the abstract, and
the proof make the intended order `forall c d, exists sequence` explicit. The statement phase must
record this cross-edition wording difference and freeze the intended ordered binders rather than
relying on English surface order.

## Definition and conclusion crosswalk

| Source location | Source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Section 2.3, pp. 310-311 | bipartition sides have respective degrees `c` and `d` | finite graph, two vertex sets, coverage/disjointness, side degree predicates | exact carrier and graph representation open |
| Section 2.3, p. 310 | definitions require `c,d >= 2` | natural-number bounds | theorem later strengthens these to `>= 3` |
| Section 2.3, p. 310 | trivial eigenvalues are `+sqrt(c*d)` and `-sqrt(c*d)` | real adjacency matrix and eigenvalue multiset | multiplicity/removal encoding open |
| Section 2.3, p. 310 | Ramanujan bound is `abs(lambda) <= sqrt(c-1)+sqrt(d-1)` for every nontrivial eigenvalue | Hermitian eigenvalue enumeration and real inequality | exact subtraction/coercion convention open |
| Lemma 5.4, p. 316 | a complete `(c,d)`-biregular graph is the base Ramanujan graph | complete bipartite base construction | proof component only |
| Theorem 5.3, p. 316 | a suitable 2-lift preserves the upper universal-cover spectral bound | graph lift and old/new eigenvalue bridge | proof component only |
| Theorem 5.5, p. 316 | infinite sequence of `d`-regular bipartite Ramanujan graphs for every `d >= 3` | specialization with equal side degrees | weaker special case, not root |
| Theorem 5.6, pp. 316-317 | infinite sequence for every pair `c,d >= 3` | universally quantified size-growing graph family | exact primary root candidate |
| proof of Theorem 5.6, pp. 316-317 | repeated 2-lifts produce a larger graph, hence a genuinely growing sequence | strict vertex-cardinality growth | intended nonvacuity bridge to freeze |

## Graph-model boundary

The paper treats ordinary finite graphs in the main result. It does not license replacing Theorem
5.6 by a multigraph theorem with loops or parallel edges. The later paper *Interlacing Families IV:
Bipartite Ramanujan Graphs of All Sizes* uses unions of matchings and explicitly notes that its
graphs may have multiple edges. That distinction is proposition-changing.

The source wording `infinite sequence` is also stronger than merely inhabiting `Nat -> Graph`:
Theorem 5.6 starts from a complete biregular graph and repeatedly takes a 2-lift with twice as many
vertices. The formal target must retain an equivalent nonrepetition or unbounded-size condition.

## Neighbor-name boundary

The repository contains another item with the same displayed MSS name, `THM-M-0339`, whose gloss
is a positive Kadison-Singer solution. Its existing source crosswalk explicitly identifies
`THM-M-0886` as the separate bipartite Ramanujan-graph result. Neither dossier inherits statement
or proof credit from the other.

## Required source admission

The statement phase must preserve one lawful immutable edition, select Theorem 5.6 and its
incorporated definitions or record an approved correction, transcribe the ordered binders,
hypotheses, conclusion, graph conventions, eigenvalue multiplicities, and boundary cases, search
for relevant corrections or errata, and obtain independent review. It must then freeze and
mutation-test the same exact Lean expression. Until those gates pass, the canonical mathematical
and Lean targets remain null and the source classification remains `H1`.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
adjacent graph and spectrum APIs. A bounded case-insensitive search for `Ramanujan`, `biregular`,
and the authors' names found no target-named declaration in repo-local Lean or pinned mathlib. This
is intake discovery only; the precommitted exhaustive anchor audit and external-project review
remain open.
