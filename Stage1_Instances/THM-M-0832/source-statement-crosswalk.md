# Source-statement crosswalk

## Repository provenance

`Docs/researches/math_theorems.md:6110-6115` is the complete catalog record. It names the
Stoer-Wagner algorithm, gives `Stoer/Wagner`, `1994`, and the gloss `全局最小割的确定性算法`
("a deterministic algorithm for the global minimum cut"), and labels it `已验证`. Git history
places all six uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:22712-22737` repeats that metadata and explicitly leaves exact definitions,
premises, proof route, dependencies, equivalent statements, axioms, machine status, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets this target
to `L0 / rework_required`.

These files establish the target's identity and intake eligibility. They do not state a theorem.

## Primary-source identity

The catalog year matches Mechthild Stoer and Frank Wagner, *A Simple Min Cut Algorithm*, in
*Algorithms - ESA '94*, Lecture Notes in Computer Science 855 (1994), pages 141-147, DOI
`10.1007/BFb0049404`. Crossref confirms the title, authors, year, venue, pages, and publisher. No
full preliminary text or exact theorem passage is admitted here.

The expanded source inspected for mathematical scope is Mechthild Stoer and Frank Wagner,
*A Simple Min-Cut Algorithm*, *Journal of the ACM* 44(4) (July 1997), pages 585-591, DOI
`10.1145/263867.263872`. Its first-page note says that a preliminary version appeared at ESA 1994,
LNCS 855, pages 141-147. The observed seven-page PDF has SHA-256
`c70e66134f25a5eec5317eb6377ef03c1bfb4c568f01bafcc025c38138d76789`.

The expanded version is a strong primary source for reconstructing the intended algorithm, but it
does not itself decide which conjunction the catalog intends. Edition comparison, correction and
errata review, exact incorporated-definition mapping, and independent mathematical review remain
open. It therefore supports provisional `H1`, not `H0`.

## Component crosswalk

| Catalog or source component | Pinpoint source meaning | Intake assessment |
|---|---|---|
| global minimum cut | JACM p.585: a nontrivial partition of `V` minimizing the sum of weights of crossing edges | direct family match; exact Lean cut encoding open |
| input graph | JACM p.586, section 2: ordinary undirected graph; every edge has nonnegative real weight | direct source domain; simple versus multi-edge formal representation open |
| deterministic algorithm | JACM pp.586-587: maximum-adjacency phases, phase cuts, merge the final two vertices, keep the lightest phase cut | algorithm family identified; executable relation and ties open |
| contraction recurrence | JACM p.586, Theorem 2.1 | source proof component, not the selected root by itself |
| phase correctness | JACM pp.587-588, Lemma 3.1: each phase cut is a minimum `s`-`t` cut for the last two vertices | source proof component, not yet formalized |
| end-to-end result | JACM pp.586-588: Theorem 2.1 plus Lemma 3.1 justify repeated contraction and the lightest phase cut | likely root family; exact statement and source conjunction open |
| runtime | JACM p.588, section 4: phase and total bounds using a priority queue and Fibonacci heaps | credible source claim; catalog does not say it belongs to the root |
| year 1994 | JACM p.585 footnote and Crossref DOI `10.1007/BFb0049404` identify the preliminary ESA version | provenance match, not proof credit by itself |
| `已验证` | untrusted catalog status | no H or M credit |

## Lean crosswalk

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the bounded intake
probe checks:

| Pinned declaration | Possible role | Missing bridge |
|---|---|---|
| `SimpleGraph` | ordinary loopless undirected adjacency relation | edge weights and contraction semantics |
| `SimpleGraph.edgeSet` / `edgeFinset` | finite undirected edge carrier | cut predicate and crossing-weight sum |
| `SimpleGraph.neighborSet` / `neighborFinset` | adjacency neighborhood | weighted tightness and maximum-adjacency selection |
| `SimpleGraph.degree` | unweighted local cardinality | weighted connectivity is not vertex degree |
| `SimpleGraph.IsEdgeReachable` / `IsEdgeConnected` | deletion-based unweighted edge connectivity | no global weighted cut, witness, contraction, or algorithm |

The `IntakeProbe.lean` checks elaborate in the pinned environment. They declare no theorem and give
no root proof credit. A bounded case-insensitive search found no tracked Lean declaration or source
documentation matching Stoer-Wagner, minimum/global cut, maximum adjacency, cut weight/capacity, or
vertex contraction in the local project or pinned mathlib. That is intake discovery only, not the
exhaustive immutable anchor audit required downstream.

## Required statement decision

Before statement elaboration, accountable source and graph-algorithm reviewers must compare the
1994 and 1997 versions or explicitly approve the expanded source, select the exact correctness,
termination, witness, and complexity clauses, map every definition and premise, audit corrections
and errata, and approve all representation and boundary decisions in `scope-map.md`. A Lean reviewer
must then freeze one expression with minimal pinned imports, checked transports, an environment
fingerprint, and the four required mutation classes.

No canonical statement, `H0`, `M0`, `R0`, audit completion, or theorem completion is claimed.
