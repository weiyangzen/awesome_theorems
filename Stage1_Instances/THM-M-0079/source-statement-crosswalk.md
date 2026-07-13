# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:582-587` supplies exactly the Chinese title
`尼尔森-施莱尔定理`, the attribution Jakob Nielsen/Otto Schreier, the year 1921, the claim
`自由群的子群仍是自由群`, importance "high," and status `已验证`. Git history attributes all
six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:2271-2296` repeats the claim while leaving the formal system, logical
foundation, exact definitions and premises, proof process, dependencies, equivalent formulations,
axioms, classical-choice use, machine status, and artifact links open. The rev-5.6 manifest carries
`已验证` only as `source_status_untrusted` and resets the target to `L0 / rework_required`.

The one-sentence claim is sufficiently specific to identify the conventional unrestricted theorem
family, but not an exact proposition: the repository gives neither explicit quantifiers nor a
definition of free group, cited edition, theorem/page, definition chain, proof mapping, correction,
erratum, translation review, or accountable source reviewer.

## Primary-source lead and historical discrepancy

Crossref metadata for DOI `10.1007/BF02952517` identifies Otto Schreier, *Die Untergruppen der
freien Gruppen*, *Abhandlungen aus dem Mathematischen Seminar der Universitaet Hamburg* 5(1),
161-183, printed December 1927. The observed Crossref response had SHA-256
`84b9c86323a71c956b5fc1dda056a4c876404b5529802f2e2cc2d19c8a02b3f7`. An attempt to access the
EuDML article page returned HTTP 403, so no primary theorem text or proof was inspected.

This lead exposes a material discrepancy: the repository gives 1921 and joint attribution for an
unrestricted claim, whereas an unpinned secondary lead encountered during intake associates 1921
with Nielsen's finitely generated case and 1927 with Schreier's general result. Because that lead
was not preserved as durable evidence, it is a question for source audit rather than an admitted
historical fact. The observed Crossref record reports bibliographic fields, not theorem wording or
that historical division. The source remains `H1`; the downstream source audit must inspect primary
texts before correcting attribution, dating, or source ownership.

## Component crosswalk

| Repository phrase | Mathematical component | Pinned Lean surface | Current assessment |
|---|---|---|---|
| free group | a group admitting a free basis | `IsFreeGroup G`, `FreeGroupBasis` | selected statement vocabulary; historical source-definition mapping open |
| subgroup | an arbitrary subgroup with inherited group structure | `H : Subgroup G` and its subtype | selected without finiteness or normality restriction |
| remains free | existence of a free basis for the subgroup | `IsFreeGroup H` | selected conclusion; basis-existence iff checked |
| conventional unrestricted reading | all ambient free groups and all subgroups | universe-polymorphic declaration | exact formal target frozen pending master acceptance |
| 1921 / joint attribution | historical metadata | documentation and provenance only | raises a question against the unpreserved 1927 general-result lead; review required |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H or M credit |

## Pinned Lean candidate

At manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, source file
`Mathlib/GroupTheory/FreeGroup/NielsenSchreier.lean` says its main result is that a subgroup of a
free group is free and exposes:

```lean
instance subgroupIsFreeOfIsFree {G : Type u} [Group G] [IsFreeGroup G]
    (H : Subgroup G) : IsFreeGroup H
```

The file SHA-256 is `e777c40c3902fd54747eac57d2952b985aff464e5d6bf803c5c78037e4c0c847`.
`IntakeProbe.lean` checked the declaration, the underlying `IsFreeGroup` and `FreeGroupBasis`
interfaces, and a proposition-shaped application. `#print axioms` reported `propext`,
`Classical.choice`, and `Quot.sound`. Mathlib's `docs/1000.yaml` also maps the Nielsen-Schreier
title to this declaration.

This is a credible candidate for a later `M0-W` result, not accepted machine closure. The statement
phase now freezes exact target identity and transports without importing this proof-bearing module.
The anchor audit must inspect the immutable terminal body, dependency and trust closure, source
boundaries, and placeholder/unsafe status; proof and validation phases must install and validate an
approved wrapper. Until then the root remains `M3` with an empty accepted proof state.

## Source gate

Before root `H0`, an accountable independent reviewer must preserve an immutable primary proof
source for the unrestricted claim; pinpoint and transcribe the exact theorem, definitions, and
assumptions; map the conclusion and every proof node; and inspect translations, corrections, and
errata. Separately, catalog-provenance reconciliation must inspect the relevant Nielsen and
Schreier primary sources to establish whether and where finite generation was removed and to resolve
the repository's attribution and date. The rank/index formula must remain outside this root unless
a separately accepted target change explicitly adds it.
