# Source-statement crosswalk

## Repository source record

The complete repository record is `Docs/researches/math_theorems.md:6791-6796`. Git history traces
all six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

| Catalog field | Received value | Intake consequence |
|---|---|---|
| title | `Burnside引理` | Names the Burnside-lemma family, but not one proposition. |
| attribution | William Burnside | Historical metadata only; no work, edition, or locator is cited. |
| time | 1897 | Historical metadata only; it does not identify a text or theorem passage. |
| statement | `群作用下的轨道计数` | Identifies group-action orbit counting but omits the formula, domains, binders, and assumptions. |
| importance | high | Scheduling metadata only. |
| formalization status | `已验证` | Explicitly untrusted; supplies no human-source or kernel credit. |

The generated record at `Docs/Stage0_Blueprint.md:25336-25361` repeats the gloss while explicitly
leaving the formal system, foundation, exact definitions and premises, proof route, dependencies,
alternate forms, axioms, machine status, and artifact links open. It therefore adds no proposition
or proof detail.

## Human-source boundary

zbMATH Open record 2672861 identifies a matching primary-book lead: William Burnside, *Theory of
Groups of Finite Order*, Cambridge University Press, 1897, xvi + 388 pages. Its selected normalized
metadata has SHA-256 `12a5a1bfadfccce00e28f3feaa4a3f5171bdcbd6c0ffc5ba8ee5668a09bab9da`.
This names a mathematical source consistent with the catalog attribution and year and supports the
minimum H1 source lead.

The book text itself was not admitted. There is still no immutable edition, exact
theorem/section/page locator, incorporated definition chain, assumption map, complete proof
boundary, attribution-history analysis, correction or errata audit, or independent source review.
The provisional human status is consequently `H1`, not `H0`.

An H0 packet must preserve an accessible immutable source, identify the exact statement and proof
passage, map every domain and assumption to the selected formal root, distinguish multiplication,
average, and bijection forms, audit corrections and naming/attribution issues, and obtain an
independent qualified review.

## Component crosswalk

| Catalog component | Candidate mathematical component | Pinned Lean surface | Intake status |
|---|---|---|---|
| group action | a group `G` with an action on a carrier `X` | `[Group α] [MulAction α β]` | direct candidate context; exact source binders unapproved |
| fixed elements | points `x` such that `g • x = x` | `MulAction.fixedBy β g` | definition located; source convention unapproved |
| orbits | equivalence classes under the same-orbit relation | `Quotient (MulAction.orbitRel α β)` | direct candidate; quotient convention unapproved |
| orbit counting | number of those quotient classes | `Fintype.card (Quotient (MulAction.orbitRel α β))` | direct natural-cardinality candidate |
| Burnside formula | sum of fixed counts equals orbit count times group size | `MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group` | exact-topic pinned theorem; candidate only |
| structural form | fixed-pair sigma type is equivalent to orbit quotient times group | `MulAction.sigmaFixedByEquivOrbitsProdGroup` | proof-supporting candidate; canonical status open |
| `已验证` | untrusted inventory label | no declaration or proof body | no H, M, or R credit |

## Pinned Lean candidate

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the direct import
`Mathlib.GroupTheory.GroupAction.Quotient` exposes:

```text
MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group
  (α : Type u) (β : Type v)
  [Group α] [MulAction α β] [Fintype α]
  [(a : α) → Fintype (MulAction.fixedBy β a)]
  [Fintype (Quotient (MulAction.orbitRel α β))] :
  (∑ a, Fintype.card (MulAction.fixedBy β a)) =
    Fintype.card (Quotient (MulAction.orbitRel α β)) * Fintype.card α
```

The source comment explicitly calls this Burnside's lemma and describes it as the average number
of elements fixed by each group element equaling the number of orbits. The immediately preceding
`sigmaFixedByEquivOrbitsProdGroup` constructs the bijection used by the three-rewrite proof. The
probe reports `[propext, Classical.choice, Quot.sound]` for both direct declarations. These facts
make the candidate unusually strong, but intake has not frozen source identity, inspected the
complete transitive terminal-body provenance, accepted its axiom profile, or checked a wrapper for
the chosen root. They therefore support `M3`, not M0.

The multiplication theorem, average/division form, and structural equivalence are not credited as
interchangeable until the statement phase selects one and checks every required direction with the
precise finiteness and arithmetic conventions. The additive analogues are alternate interfaces,
not extra proof credit.

## Neighbor and namesake boundary

Polya enumeration (`THM-M-0928`) uses Burnside-style orbit counting but is not the same theorem.
Orbit-stabilizer and the conjugation class equation are supporting or specialized results, not
substitutes. Burnside's `p^a q^b` solvability theorem (`THM-M-0069`) and Burnside transfer concern
finite-group structure rather than action-orbit counting. No statement or receipt transfers from
those targets.

## Required admission

The statement phase must preserve and independently review an exact human source, select the
canonical form, freeze every ordered binder, hypothesis, conclusion, arithmetic and quotient
convention, and boundary case, then elaborate that same proposition with minimal pinned imports.
It must serialize the expression and environment, compile each credited transport, and run the
required mutations. The anchor-audit phase must separately inspect the terminal body, dependencies,
axioms, placeholders, provenance, licenses, and trust closure. Until then the canonical target is
null and no proof state is accepted.
