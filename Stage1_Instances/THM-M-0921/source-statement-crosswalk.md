# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6735-6740` supplies exactly the title `卡塔兰数` (Catalan
numbers), attribution to Eugene Catalan, year 1838, gloss `多种组合问题的计数` (counting in many
combinatorial problems), importance `高`, and status `已验证`. All six uncited lines originate in
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no formula,
object definition, binders, hypotheses, conclusion, bibliography, theorem locator, proof boundary,
correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25120-25145` repeats that gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof route, dependencies, equivalent forms,
axioms, machine status, and artifact links open. Its generic theorem-tree language is planning
metadata. The rev-5.6 manifest preserves `已验证` only as untrusted source status and resets this
target to `L0 / rework_required`.

## Inspected subject-family lead

Richard P. Stanley, *Catalan Addendum*, version of 25 May 2013, author-hosted PDF observed on
2026-07-13, was inspected. Page 1 defines
`C_n = (1/(n+1)) binom(2n,n)` and its generating function, and says that its numbered
combinatorial interpretations continue Exercise 6.19 of *Enumerative Combinatorics*, volume 2.
The following pages list many different finite structures counted by Catalan numbers.

The observed PDF SHA-256 is
`1d0e3cff08cbc7244d282e2c817f15fa3829b05941efaa4218ead49c9ec0e2b4`. The copy is a
mutable author-hosted source lead and was not added to the repository. The catalog does not cite
this edition, Exercise 6.19, a particular interpretation, or a proposition combining them. The
addendum also warns that problem numbers change between versions. A lawful immutable edition,
pinpoint proof source, correction audit, clause mapping, and independent review remain open. This
lead therefore helps disambiguate the family but does not establish `H0`.

The catalog's attribution to Eugene Catalan in 1838 is preserved as catalog metadata. No 1838
primary publication, exact passage, translation, formula, proof, or errata was inspected or
credited, so the historical attribution is not a source-statement crosswalk.

## Clause crosswalk

| Catalog element | Source-family component | Prospective Lean surface | Intake result |
|---|---|---|---|
| `卡塔兰数` | conventional sequence `C_n` | `catalan : Nat -> Nat` | exact definition and source transport not selected |
| `多种` / "many" | a collection of distinct interpretations | separate cardinality theorems or an explicit indexed schema | no finite package, index family, or composition rule supplied |
| `组合问题` | trees, Dyck paths, triangulations, and many other objects under differing conventions | finite types, size fibers, equivalences, and cardinalities | object family and conventions open |
| `计数` | equality of a finite cardinality with `C_n` | `Fintype.card` or `Finset.card` equality | carrier, quotient, labels, size statistic, and binders open |
| `1838` / Eugene Catalan | historical attribution | provenance only | no primary passage inspected; no H credit |
| `已验证` | untrusted inventory label | source review and exact kernel evidence would be required | no H or root M credit |

## Pinned Lean candidates, not a selected root

At the pinned mathlib revision, `Mathlib.Combinatorics.Enumerative.Catalan` provides the recursive
definition and theorems `catalan_succ`, `catalan_eq_centralBinom_div`,
`succ_mul_catalan_eq_centralBinom`, and `Tree.treesOfNumNodesEq_card_eq_catalan`.
`Mathlib.Combinatorics.Enumerative.DyckWord` provides
`DyckWord.card_dyckWord_semilength_eq_catalan`, and
`Mathlib.RingTheory.PowerSeries.Catalan` provides
`PowerSeries.catalanSeries_sq_mul_X_add_one`.

`IntakeProbe.lean` authenticates these declarations in the pinned environment. They are credible
machine-checked candidates for several different precise theorems, but intake does not award root
credit: the repository gloss has no exact proposition to which normalized statement identity can
be compared. Their terminal bodies, transitive dependencies, axioms, and source fidelity still
require the downstream anchor audit after statement selection.

## Source gate

Before ordinary theorem execution, accountable reviewers must preserve an immutable approved
source edition and choose one exact proposition or explicit multi-root package. They must map every
definition, binder, hypothesis, conclusion, interpretation, size convention, quotient, boundary
case, proof source, correction, and erratum; independently approve fidelity to `THM-M-0921`; and
state what the selected root does not include. Only then may the statement phase freeze minimal
imports, the elaborated expression and environment hashes, checked alternate encodings, and the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
