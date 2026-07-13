# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1815-1820` supplies exactly the title `科罗纳问题`, Lennart
Carleson, 1962, the gloss `H^∞的极大理想空间` ("the maximal ideal space of H-infinity"),
importance "high," and status `已验证`. Git blame attributes all six uncited lines to repository
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, formula,
domain, definition of `H^∞`, topology, ordered hypotheses, conclusion, proof boundary, correction
history, or formal artifact.

`Docs/Stage0_Blueprint.md:6977-7002` repeats the gloss, classifies it as a "problem / decision
proposition," and explicitly leaves the target system, foundation, precise definitions and
premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact links
open. Its generated planning language is not theorem evidence. The rev-5.6 manifest preserves
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Crossref identifies Lennart Carleson, *Interpolations by Bounded Analytic Functions and the Corona
Problem*, *The Annals of Mathematics* 76(3) (November 1962), DOI `10.2307/1970375`; its metadata
reports start page 547. The metadata matches the catalog author, year, and subject and is a credible
primary-source lead, but even the complete pagination must be reconciled against the primary
edition. It is discovery evidence only: no immutable primary text, exact theorem/page passage,
incorporated definition chain, assumption-to-conclusion mapping, corrections or errata, or
independent review was obtained. It supplies no H0 credit and does not select a root.

## Component crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `科罗纳问题` | select a solved theorem rather than a problem-family name | one exact canonical `Prop` | family identified; root open |
| Lennart Carleson / 1962 | identify the exact primary passage and correction history | immutable source identity and version | matching paper metadata only |
| `H^∞` | fix the domain and the algebra of bounded analytic functions | carrier, analytic and bounded predicates, normed commutative algebra, completeness | algebra not selected or constructed |
| `极大理想空间` | choose maximal ideals, continuous characters, or Gelfand spectrum and their topology | `Ideal`, `Ideal.IsMaximal`, `WeakDual.characterSpace`, topology, checked equivalence | encoding and topology open |
| domain points | decide whether disc points act by evaluation | evaluation character and continuity/multiplicativity proofs | absent from the catalog |
| possible density reading | state that evaluations are dense in the maximal-ideal/character space | `DenseRange`, closure equality, or equivalent exact predicate | conclusion not stated by the catalog |
| possible Bezout reading | state the finite corona condition and bounded analytic coefficient conclusion | finite indexed functions, lower bound, existential coefficient family, identity | separate target uses this reading; not inherited |
| equivalence of readings | select required implication directions and assumptions | kernel-checked transports | no witness credited |
| `已验证` | untrusted inventory assertion | no proof object | explicitly rejected as evidence |

## Duplicate-target conflict

`Docs/researches/math_theorems.md:2710-2715` separately defines `THM-M-0373`, `Corona定理`, with
the same attribution and year and the gloss `H^∞的Corona问题`. Its dossier selected the classical
finite-generator Bezout target and records maximal-ideal-space density only as an unchecked
alternate. The two catalog entries are likely duplicates or overlapping formulations, but that is
an integration decision. It does not authorize this intake to merge IDs, silently replace the
maximal-ideal-space gloss by the Bezout statement, or inherit any source or machine evidence.

## Candidate formulations and conflicts

The slogan "maximal ideal space of H-infinity" could intend density of disc evaluations, the
equivalent finite Bezout theorem, a description of characters, or merely the object involved in
the historical problem. Those readings require different binders and infrastructure. Even within
the classical theorem, maximal ideals versus continuous characters and weak-star versus quotient
topologies require checked bridges. The catalog supplies none of these choices.

## Required source correction

Before statement work, accountable reviewers must preserve and hash an immutable primary edition,
pinpoint the exact theorem and every incorporated definition, map all domains, binders, premises,
topologies, equivalences, conclusions, and boundary cases, inspect corrections and errata, decide
the relationship to `THM-M-0373`, and obtain independent source and duplicate-scope review. Only
then may the statement phase encode and mutation-test a canonical Lean expression. Until that
correction, the received target is provisionally `H5`, while machine and readability states remain
`M4` and `R4`.

## Lean intake boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the API-only probe
checks the unit disc, analytic-on-a-set predicate, generic character space, maximal-ideal predicate,
maximal-ideal-to-character map, and density predicate. These are encoding ingredients, not an
`H^∞` construction, evaluation embedding, corona statement, or proof. A bounded exact-topic search
found no repo-local or pinned-mathlib corona declaration. This is not a downstream immutable
anchor audit and carries no negative-result or proof credit.
