# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md:256-261` records only:

- title: Serre's conjecture;
- attribution: Jean-Pierre Serre;
- year: 1955;
- gloss: projective modules over polynomial rings are free;
- importance: high;
- untrusted formalization label: verified.

All six lines originate in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:1019-1044`
repeats the catalogue record while explicitly leaving exact definitions, premises, proof route,
equivalent forms, axioms, machine status, and artifact links open. These records establish identity
and discovery provenance only.

## Historical source leads

Crossref metadata for DOI `10.2307/1969915` identifies Jean-Pierre Serre, "Faisceaux Algebriques
Coherents," *Annals of Mathematics* 61(2) (1955), starting at page 197. The retrieved metadata
payload had SHA-256 `88a626e46ae238bea3a20c855a2ca7823162f99bc7347b7d1e21a6c02b61a386`.
The article text and the often-cited problem passage were not preserved and independently inspected
during intake, so this is a bibliographic lead rather than H0 evidence.

Crossref metadata for DOI `10.1007/BF01390008` identifies Daniel Quillen, "Projective modules over
polynomial rings," *Inventiones Mathematicae* 36(1) (1976), pages 167-171. The retrieved metadata
payload had SHA-256 `c7e501fdb9473fadc536a6a99c7b5696e3740115a5f1d60cf1392ae9e004efc4`.
An earlier related paper is A. A. Suslin, "On projective modules over polynomial rings," DOI
`10.1070/SM1974v022n04ABEH001708`. Because its 1974 scope was not inspected, it is not represented
as the later full solution. A separate full-solution lead is Suslin, "Projective Modules Over
Polynomial Rings Are Free," *Doklady Akademii Nauk SSSR* 229 (1976), 1063-1066. These locators
identify candidates only. No exact theorem passage, definition chain, hypothesis map, proof
boundary, translation history, correction search, or independent review is accepted here.

## Clause crosswalk

| Catalogue phrase | Required source decision | Pinned Lean surface | Intake status |
|---|---|---|---|
| "polynomial rings" | coefficient ring, number/index type of variables, commutativity and unit conventions | `Polynomial k` or `MvPolynomial sigma k` | APIs located; encoding not selected |
| "modules" | left/right convention, universes, additive and scalar structures | `Module R P` typeclass context | prospective context only |
| "projective" | exact source definition and equivalent-form transport | `Module.Projective R P` | definition available; source transport open |
| hidden finiteness | finite generation/presentation or another smallness premise | candidate `Module.Finite R P` or related predicates | absent from catalogue; cannot be invented |
| "are free" | basis existence, finite basis/rank behavior, same scalar ring | `Module.Free R P` | conclusion API available; no implication theorem found |
| theorem identity | original question versus Quillen/Suslin solution or later generalization | no canonical declaration | unresolved |

The pinned declaration `Module.Projective.of_free` runs from `Module.Free R P` to
`Module.Projective R P`. It authenticates the relationship of the two APIs but is the reverse of
the target direction and receives no root-proof credit. Mathlib's `docs/1000.yaml` contains only a
title row for the Quillen-Suslin theorem; it is not a declaration or evidence receipt.

## Required source work

The statement phase must lawfully preserve an exact source edition; identify the theorem/problem
number and pages; crosswalk all definitions, binders, hypotheses, and the conclusion; distinguish
original, independently solved, and generalized formulations; check translations, corrections,
and errata; and obtain independent review. Only then may one exact Lean proposition and any checked
alternate-form transports be frozen. Until that work is complete, the source level remains H1 and
neither source lead supports H0 or machine credit.
