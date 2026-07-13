# THM-M-0867 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6355-6360` records only:

- title: `Robertson-Seymour图子式定理`;
- attribution: Neil Robertson and Paul Seymour;
- year: 2004;
- gloss: `图子式良拟序定理`;
- importance: high;
- untrusted formalization label: `已验证`.

All six lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:23657-23682`
repeats the gloss while leaving the precise definitions and premises, proof route, dependencies,
equivalent formulations, axioms, machine status, and artifact links open. These records establish
catalog identity only.

## Primary-source lead

Neil Robertson and P. D. Seymour, *Graph Minors. XX. Wagner's conjecture*, Journal of
Combinatorial Theory, Series B 92(2) (2004), pages 325-357,
DOI `10.1016/j.jctb.2004.08.001`, is a matching primary work. An author-hosted 34-page PDF headed
"February 1988: revised August 11, 2004" was inspected on 2026-07-13. It is 251,605 bytes with
SHA-256 `327694f043a8809dfb0255171c470ae4ba5b15d7fedbad861c43f1f3a05caa91`.

The inspected passages are:

- abstract: "for every infinite set of finite graphs, one of its members is isomorphic to a minor
  of another";
- Introduction, first paragraph: the same Wagner-conjecture wording and the parenthetical "all
  graphs in this paper are finite";
- Theorem 10.5, paper page 29: every countable sequence of directed graphs has `j > i >= 1` such
  that `G_i` is isomorphic to a minor of `G_j`; the preceding sentence says this immediately
  implies the standard undirected form and defines the directed minor operation via a subgraph and
  edge contractions.

Crossref metadata observed for the DOI confirms the authors, title, journal, volume, issue, page
range, and November 2004 publication. The observed JSON response has SHA-256
`ca748048c60371506a6189b73555d68cfe88c6f7def29a14674e4b71bc6927fa`.

This is a strong primary-source lead, but not H0. The author-hosted draft has not been reconciled
byte-for-byte with the version of record; the standard undirected minor definition and every
incorporated convention have not been transcribed; set/sequence/WQO equivalence and graph-model
choices are not checked; corrections and errata are not closed; and no independent reviewer has
approved the mapping.

## Clause crosswalk

| Catalog clause | Primary-source lead | Prospective Lean component | Intake status |
|---|---|---|---|
| "graphs" | abstract says finite graphs; paper works with graph, directed-graph, and hypergraph machinery | a sigma/canonical type of finite graphs, likely built from `SimpleGraph` | graph model and representation open |
| "minor" | "isomorphic to a minor"; directed version describes subgraph plus contractions | a new or audited minor predicate with checked orientation | absent from pinned simple-graph API search |
| "well-quasi-order" | abstract uses an infinite set; Theorem 10.5 uses a countable sequence with ordered indices | `WellQuasiOrdered minorRelation` or an exact alternate expression | transport and preorder conditions open |
| quantifier | every infinite set / every countable sequence | `forall G : Nat -> FiniteGraph, exists i j, i < j and ...` | candidate shape only |
| conclusion | earlier graph is isomorphic to a minor of later graph in Theorem 10.5 | relation must account for isomorphism and differing vertex types | representation and exact relation open |
| `已验证` | repository metadata only | no Lean declaration or proof object | no H or M credit |

## Formal candidate crosswalk

| Pinned declaration | Candidate role | Missing gate |
|---|---|---|
| `WellQuasiOrdered` | generic sequence definition of WQO | finite-graph carrier and exact minor relation |
| `wellQuasiOrdered_iff_exists_monotone_subseq` | alternate characterization for a preorder | preorder instance and checked source relationship |
| `SimpleGraph.Iso` | graph isomorphism witness | heterogeneous finite-graph packaging or quotient transport |
| `SimpleGraph.induce` | induced graph on a vertex subset | deletion/contraction closure and exact minor semantics |
| `SimpleGraph.deleteEdges` | deletion of selected edges | vertex deletion, contraction, transitive closure, and isomorphism |
| `SimpleGraph.map` | graph pushforward along a function | proof that any use models precisely the selected contractions |

Before statement acceptance, reviewers must select one admitted source proposition and graph/minor
definition, freeze every binder and boundary case, elaborate it under minimal pinned imports,
serialize its expression and environment, compile all credited transports, and run the required
removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
