# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:5542-5547` supplies exactly the title `跳跃算子`, attribution
Stephen Kleene/Emil Post, year 1954, gloss `图灵度的跳跃`, importance `高`, and status `已验证`.
All six uncited lines originate at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record has no bibliography, formula,
definitions, theorem locator, assumptions, conclusion, proof boundary, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:20542-20567` projects the record as `THM-M-0752` while explicitly leaving
the formal system, precise definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine state, and artifact links open. Its generic statement that a closed result is known
and the source label `已验证` supply no `H`, `M`, or `R` credit under rev-5.6.

## Literal crosswalk

| Repository element | Mathematical information still required | Prospective Lean surface | Intake result |
|---|---|---|---|
| `跳跃算子` | one proposition about the operator rather than its name | an exact `Prop`, not merely a definition | root not selected |
| `图灵度` | sets/predicates or partial functions, reducibility, equivalence, quotient transport | `TuringReducible`, `TuringEquivalent`, `TuringDegree` plus checked encodings | adjacent pinned vocabulary only |
| `跳跃` | oracle-machine numbering and relativized diagonal halting set | a new source-mapped jump construction | absent |
| induced degree map | representative invariance and quotient lifting | a checked well-defined operation | absent |
| possible theorem | noncomputability, strictness, monotonicity, completeness, or a selected package | source-identical ordered binders and conclusion | ambiguous |
| Kleene/Post, 1954 | exact work, theorem/page, genealogy, definitions, and corrections | source provenance only | bibliographic lead |
| `已验证` | claimed formal status | accepted kernel evidence would be required | explicitly rejected |

## Primary-source lead

Crossref metadata identifies S. C. Kleene and Emil L. Post, "The Upper Semi-Lattice of Degrees of
Recursive Unsolvability," *The Annals of Mathematics* 59(3) (May 1954), starting at page 379, DOI
`10.2307/1969708`. The complete 379-407 page range is independently present in the inspected
Spring 2024 SEP bibliography, not in the Crossref response. The authors, date, and degree subject
closely match the catalog. The retrieved metadata response had SHA-256
`24e7b0e162ef53d32b82438ce194652105e552145d3e6d5a46448e5e0ed26a4b`.

The version-of-record service returned an automated-access block, and Semantic Scholar reported no
open-access PDF. No theorem passage, definition, page-level jump claim, assumption, proof step,
correction, or erratum was inspected. The paper is therefore a primary bibliographic lead only,
not `E4`, `H0`, or evidence that the catalog intended any one proposition listed in the scope map.

## Authoritative secondary lead

Walter Dean and Alberto Naibo, "Recursive Functions," *Stanford Encyclopedia of Philosophy*,
Spring 2024 archive, Section 3.5.2, Proposition 3.7, was inspected at its immutable archive URL. It
defines `A'` as the diagonal halting problem relativized to `A`, explains the induced notation on
degrees, and separately lists relative enumerability/noncomputability, representative invariance,
strict increase, monotonicity, and relative completeness. The archived HTML had SHA-256
`7d856ecda491ab83814622f4a75d277552b8750816412bca215b4a461d0b0af1`.

This source confirms the standard family and shows why the catalog wording is propositionally
ambiguous. It is secondary and does not say that the catalog's 1954 label selects all or any one of
Proposition 3.7's clauses. It therefore remains discovery evidence, not a source-frozen root or H0.
An Encyclopedia of Mathematics entry gives a related maximal-relative-c.e. characterization and
monotonicity, again demonstrating candidate breadth rather than selecting a target.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Computability.TuringDegree` provides:

| Declaration | Exact role | Intake boundary |
|---|---|---|
| `RecursiveIn` | oracle-relative partial recursiveness | substrate; not a jump |
| `TuringReducible` | `f` recursive relative to singleton oracle `g` | reducibility definition only |
| `TuringEquivalent` | mutual Turing reducibility | representative relation only |
| `TuringReducible.refl` / `.trans` | preorder laws | order infrastructure only |
| `TuringEquivalent.equivalence` | equivalence proof | quotient infrastructure only |
| `TuringDegree` | antisymmetrization quotient of partial functions | degree type only |
| `TuringDegree.instPartialOrder` | partial order on degrees | no jump operation or property |

The pinned `TuringDegree.lean` SHA-256 is
`d5fd0caf5c321343ec378e2601913aec152efac58f113ce3b602dca7345b1e5c`. A bounded search of
pinned computability modules found no computability-theoretic jump declaration; unrelated machine
control-flow uses of the word "jump" were excluded. No repo-local target artifact was found. These
observations are intake discovery only, not an exhaustive anchor audit or a global absence claim.

## First blocker and retry condition

The first downstream blocker is exact source-statement identity. Accountable reviewers must
preserve a lawful immutable primary or accepted authoritative passage; choose one exact proposition;
map every definition, binder, premise, conclusion, and boundary convention; reconcile the 1954
attribution and neighboring target ownership; audit corrections and errata; and independently
approve the crosswalk. Only then may the statement phase implement any missing oracle-jump
infrastructure, elaborate the exact Lean target, minimize imports, serialize fingerprints, check
alternate encodings, and mutation-test hypotheses, domains, binder scope, and boundary cases.
