# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:547-552` supplies exactly the Chinese title `格里思定理`, Robert
Griess, the year 1982, the gloss `魔群的存在性`, importance "high," and status `已验证`. Git history
attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition of the
Monster, exact order, binders, hypotheses, conclusion, construction, proof boundary, correction
history, formal system, or machine artifact.

`Docs/Stage0_Blueprint.md:2136-2161` repeats that gloss while explicitly leaving the formal system,
logical foundation, exact definitions and premises, proof process, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic statement that a closed mathematical
result is known is planning metadata. The rev-5.6 target manifest preserves `已验证` only as
untrusted source metadata and resets the target to `L0 / rework_required`.

## Inspected primary-source lead

Robert L. Griess Jr., *The friendly giant*, *Inventiones mathematicae* **69** (1982), issue 1,
pages 1-102, DOI `10.1007/BF01389186`, is the bibliographically matching primary-paper lead.
Crossref and the publisher article page were inspected on 2026-07-13. Both identify Griess, the
title, journal, volume, issue, year, and page range. The publisher labels it an original paper, but
the inspected unauthenticated surface provides neither abstract nor article body; its full text is
not preserved under this owned path.

An earlier primary construction announcement supplies an exact statement witness: Robert L. Griess
Jr., *A construction of F1 as automorphisms of a 196,883-dimensional algebra*, *Proceedings of the
National Academy of Sciences of the United States of America* **78** (1981), issue 2, pages 689-691,
DOI `10.1073/pnas.78.2.689`, PMCID `PMC319865`. Its openly inspected abstract announces construction
of a finite simple group `F1` of order
`2^46 * 3^20 * 5^9 * 7^6 * 11^2 * 13^3 * 17 * 19 * 23 * 29 * 31 * 41 * 47 * 59 * 71`,
equal to `808017424794512875886459904961710757005754368000000000`, realized as a group of
automorphisms of a 196883-dimensional commutative nonassociative algebra over the rationals with an
associative form, equivalently of a cubic form. Because the note explicitly calls itself an
announcement, it is statement-disambiguation evidence and not a complete `H0` proof source.

Consequently this intake does not assert an exact theorem number from the unseen 1982 paper. It
does not decide whether that paper's terminal root is most faithfully encoded as existence of a
finite simple group of the Monster order, construction as a subgroup or the full automorphism group
of the Griess algebra, or a stronger package. The complete primary text, definitions, ordered
premises, construction-to-simplicity bridge, correction and errata audit, and independent source
review are required before `H0` or statement acceptance.

## Component crosswalk

| Catalog component | Primary-source question | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "existence" | existential abstract group, concrete automorphism group, or named constructed object | `Nonempty` or `Exists` over a group carrier | quantifier and witness model open |
| "Monster group" | construction, exact order, simplicity, and possibly uniqueness or recognition | `[Group G]`, `[Finite G]`, `IsSimpleGroup G`, `Nat.card G`, `MulEquiv` | defining property package open |
| Griess construction | exact 196883-dimensional algebra and its automorphism group | nonassociative algebra, linear automorphisms, invariant form | scalar field and construction data open |
| exact order | decimal integer or prime-factor expression | `Nat.card G = ...` | statement role and checked numeral identity open |
| identity of the group | equality, isomorphism class, recognition, or uniqueness | `G ≃* H` and checked transports | source scope open |
| `已验证` | untrusted inventory status | accepted source and kernel receipts would be needed | no H or M credit |

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.GroupTheory.Subgroup.Simple` supplies `IsSimpleGroup` and simplicity transport along
`MulEquiv`; `Mathlib.Data.Finite.Card` supplies `Finite` and `Nat.card` interfaces.
`IntakeProbe.lean` checks those substrate APIs and elaborates an explicitly nonterminal envelope:
existence of a finite simple group with the announcement's factorized order. That envelope remains
weaker than a source-selected Monster identity because it omits the Griess construction and any
accepted recognition or uniqueness bridge.

A bounded case-insensitive search over repository-local Lean and pinned mathlib Lean files for the
target ID, Griess, Friendly Giant, and Monster-group spellings found no terminal target declaration.
The only mathematical Monster reference found in mathlib was bibliographic prose about vertex
algebras, while unrelated model-theory files use "monster model" in a different sense. This is a
focused intake observation, not an exhaustive external anchor audit and not a global absence proof.

## Scope boundary

`THM-M-0071` covers the classification of finite simple groups. Its current intake correctly treats
this target as one sporadic branch that cannot close the classification root; conversely, generic
classification wording cannot replace the concrete Monster construction here. Thompson's
uniqueness work, the Conway-Norton moonshine conjecture, the moonshine module, and later vertex
algebra constructions may become provenance or alternate-construction nodes only after the exact
1982 target and source boundary are frozen.

The source status is `H1`, not `H0`: the theorem family and matching primary-paper lead are known,
but exact statement, assumptions, conclusion, proof boundary, corrections, and node mapping have
not been independently accepted.
