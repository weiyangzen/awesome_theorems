# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:7078-7083` supplies exactly the title `Lovász局部引理`, the
attribution Laszlo Lovasz, the year 1975, the gloss `稀疏依赖事件同时不发生的概率`, importance
"high," and status `已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, theorem
locator, formula, ordered binders, hypotheses, dependency definition, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:26416-26441` repeats the gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as
untrusted metadata and resets the target to `L0 / rework_required`.

An exact primary source-family lead was inspected: P. Erdos and L. Lovasz, *Problems and results on
3-chromatic hypergraphs and some related questions*, in *Infinite and Finite Sets*, Colloquia
Mathematica Societatis Janos Bolyai 10, Keszthely 1973, pp. 609-627 (published 1975). The complete
19-page scan observed at `https://users.renyi.hu/~p_erdos/1975-34.pdf` has 1,880,140 bytes and
SHA-256 `fc99b53c12d75066934e2f4e35c7189b35276f0a006af075010e01cffd74e2e0`.

Section 2, printed pp. 616-617, gives a finite-graph candidate lemma: attach events `A_i` to the
vertices of a finite graph of maximum degree `d`; require each `A_i` to be independent of the family
attached to its nonneighbors and `P(A_i) <= 1/(4d)`; conclude that the intersection of all event
complements has positive probability. The page image confirms the complement bars and inequality
that its OCR layer loses. The proof establishes a stronger conditional bound by induction.

This is a strong source-family and 1975 attribution match, but it is not admitted as the canonical
root or H0 evidence. It supports provisional H1 while exact mapping remains open. The repository
gloss still does not decide between this original `1/(4d)`
form, a modern symmetric corollary, the general asymmetric form, a lopsided variant, or a bundled
statement. Complete incorporated-definition and premise mapping, correction/errata audit, and
independent review remain open. Selecting the original lemma merely because it was located would
still be an unsupported target decision.

## Clause crosswalk

| Catalog component | Candidate mathematical reading | Prospective pinned Lean surface | Intake assessment |
|---|---|---|---|
| "events" | measurable sets in a probability space | `MeasurableSet`, `MeasureTheory.Measure`, `IsProbabilityMeasure` | carrier, measure, measurability, and index type open |
| "all fail to occur" | intersection of complements | `Set.compl`, `Set.iInter`, finite intersections | finite/infinite encoding and exact conclusion open |
| "probability" | positive measure or an explicit product lower bound | `MeasureTheory.Measure` with `ENNReal` values | positivity versus quantitative conclusion open |
| "sparse dependency" | graph/relation plus independence outside each neighborhood | `ProbabilityTheory.IndepSet`, `ProbabilityTheory.iIndepSet`, generated measurable spaces | dependency and independence semantics open |
| symmetric reading | common event bound and degree bound | finite graph/event data plus real/ENNReal arithmetic | common criterion and endpoints absent from catalog |
| asymmetric reading | weights `x_i` and neighbor products | finite products and per-event bounds | materially stronger/different candidate statement |
| inspected 1975 lemma | finite graph, maximum degree `d`, nonneighbor-family independence, `P(A_i) <= 1/(4d)`, positive complement-intersection probability | `SimpleGraph.maxDegree`, event-independence APIs, finite intersections | strong primary-source candidate; not canonical or H0-accepted |
| `已验证` | untrusted inventory label | source review and kernel receipts would be required | no H or M credit |

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded exact-topic
name and prose searches found no Lovasz-local-lemma declaration. The intake probe elaborates
`ProbabilityTheory.iIndepSet`, `ProbabilityTheory.IndepSet`, the finite-intersection
characterization `ProbabilityTheory.iIndepSet_iff_meas_biInter`, the disjoint-family bridge
`ProbabilityTheory.iIndepSet.indep_generateFrom_of_disjoint`, and
`ProbabilityTheory.IndepSet.measure_inter_eq_mul`, together with basic event/intersection APIs.
`Mathlib.Combinatorics.SimpleGraph.Finite` supplies `SimpleGraph.neighborFinset`,
`SimpleGraph.degree`, `SimpleGraph.maxDegree`, and `SimpleGraph.degree_le_maxDegree` for a possible
source-faithful graph encoding.

These are adjacent probability infrastructure only. They neither encode sparse graph dependency
nor select or prove a local-lemma root. The search is bounded intake discovery, not an exhaustive
mathlib or external-project anchor audit and not a global absence claim.

## Source gate

Before leaving H1, accountable reviewers must admit a lawful immutable primary or authoritative
source edition, identify the exact theorem and incorporated definitions, map every domain, binder,
hypothesis, dependency convention, numerical condition, conclusion, and boundary case, audit
corrections and attribution, and independently approve fidelity to `THM-M-0969`.

Only after that source decision may the statement phase select minimal imports, freeze an
elaborated expression and environment fingerprint, compile checked alternate encodings, and run
the required removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
