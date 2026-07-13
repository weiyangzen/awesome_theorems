# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6166-6171` supplies exactly the title `强完美图定理`, attribution
to Chudnovsky/Robertson/Seymour/Thomas, the year 2006, the gloss `完美图的禁用子图刻画`
("forbidden-subgraph characterization of perfect graphs"), importance "high," and status
`已验证`. Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, stable source
identifier, theorem/page locator, formula, definitions, binders, proof boundary, correction
history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22928-22953` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected primary source lead

Maria Chudnovsky, Neil Robertson, Paul Seymour, and Robin Thomas, *The strong perfect graph
theorem*, Annals of Mathematics 164(1) (2006), 51-229, DOI
`10.4007/annals.2006.164.51`, was inspected from the journal-hosted PDF on 2026-07-13.

- The abstract defines perfect and Berge graphs and says that the paper proves their equivalence.
- Article pages 51-52 state that all graphs in the paper are finite and simple, define the graph
  complement, holes and antiholes, define Berge graphs by even holes and antiholes, define perfect
  graphs through every induced subgraph, and state Theorem 1.2: "A graph is perfect if and only if
  it is Berge."
- Article pages 52-229 contain the proof architecture and proof. The intake inspected the statement
  boundary and opening reduction, not a node-complete proof/errata crosswalk.
- The observed journal PDF SHA-256 is
  `f70115028dea55dec5a97f3a50af82686782821a612ca672ad666a19c0eba4c2`.
- The journal DOI and bibliographic metadata match the catalog authors and year. ArXiv
  `math/0212070v1` is an earlier 2002 source lead with the same authors and abstract, but it has not
  been declared definitionally or textually identical to the published edition.

The journal-hosted copy was not added to the repository. An immutable approved source snapshot,
full incorporated-definition and premise map, correction/errata audit, proof-node crosswalk,
lawful preservation decision, and independent review remain open. The source supports provisional
`H1`, not `H0`.

## Clause crosswalk

| Catalog component | Primary-source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| graph | all graphs are finite and simple | `G : SimpleGraph V` with finite vertex type | representation, universe, and decidability open |
| perfect graph | every induced subgraph has chromatic number equal to largest-clique size | `G.induce s`, `SimpleGraph.chromaticNumber`, `SimpleGraph.cliqueNum` | exact subset/subgraph quantifier and `ENat`/`Nat` comparison open |
| forbidden subgraph | Berge means every hole and antihole has even length | cycle/walk, induced graph, complement, length and parity predicates | no pinned Berge/hole predicate found; chordless induced-cycle encoding open |
| odd hole | induced cycle of odd length at least five | future predicate combining inducedness, `Walk.IsCycle`, length, and parity | ordinary cycles or triangles are not substitutes |
| odd antihole | complement of an odd hole / odd hole in the complement | `Gᶜ` plus a checked induced-complement transport | representation and transport open |
| characterization | Theorem 1.2, perfect iff Berge | future biconditional root | source family identified; exact Lean expression not frozen |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H0 or M credit |

## Pinned Lean boundary

Pinned mathlib supplies `SimpleGraph.induce`, graph complement, `Walk.IsCycle`,
`SimpleGraph.chromaticNumber`, `SimpleGraph.cliqueNum`, and
`SimpleGraph.cliqueNum_le_chromaticNumber`. These APIs cover part of a future encoding but do not
define perfect graphs, Berge graphs, holes/antiholes, or prove their equivalence.

A bounded case-insensitive search of pinned mathlib and repo-local Lean found no exact-topic
declaration for perfect graphs, Berge graphs, odd holes/antiholes, or the strong perfect graph
theorem. Unrelated occurrences such as perfect matchings, perfect groups, or `PerfectRing` were
excluded by context. This is intake discovery only, not the later immutable formal-candidate audit
and not a global absence theorem.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an immutable approved source edition,
map every incorporated definition, binder, premise, conclusion, complement and induced-subgraph
convention, audit corrections and the published/arXiv relationship, crosswalk the proof nodes, and
independently approve fidelity to `THM-M-0840`. Only then may the statement phase freeze the exact
Lean predicates, minimal imports, elaborated expression and environment hashes, checked alternate
encodings, and required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
