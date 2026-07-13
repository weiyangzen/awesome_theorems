# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6679-6684` supplies exactly the title `容斥原理`, attribution
`众多数学家`, period `19世纪`, gloss `并集元素个数的计算公式`, high importance, and status
`已验证`. Git history attributes the uncited six-line record to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no formula, definitions, assumptions,
theorem/page citation, proof boundary, errata record, reviewer, or formal-artifact link.

`Docs/Stage0_Blueprint.md:24904-24929` repeats the gloss while explicitly leaving precise
definitions and premises, proof route, dependency graph, alternate forms, axioms, machine status,
and artifacts open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

No primary mathematical source has been identified in the repository. The generic attribution
"many mathematicians" and century are genealogy metadata, not an edition/theorem/page locator.
Consequently there is no premise-by-premise source mapping, correction/errata audit, translation
audit, or independent source review, and no H0 credit is possible at intake.

## Literal component crosswalk

| Catalog component | Candidate reading | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| `容斥原理` | general finite inclusion-exclusion principle | module `Mathlib.Combinatorics.Enumerative.InclusionExclusion` | family identity only; not exact-statement evidence |
| `并集` | union of two sets or a finite indexed union | `Finset.biUnion`, with finite index `s : Finset iota` | arity and encoding remain open |
| `元素个数` | cardinality of finite sets, perhaps cast to integers | `Finset.card` and an equality in `Int` | finiteness and coefficient convention are not stated |
| `计算公式` | alternating sum over nonempty intersections | `Finset.inclusion_exclusion_card_biUnion` | strong candidate; the formula itself is absent from the catalog |
| `已验证` | untrusted inventory label | accepted source and kernel receipts would be required | no H/M credit |

## Pinned formal lead

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source file
`Mathlib/Combinatorics/Enumerative/InclusionExclusion.lean:149-156` defines
`Finset.inclusion_exclusion_card_biUnion`. For `s : Finset iota`, `S : iota -> Finset alpha`, and
decidable equality on `alpha`, it states in integers:

```text
card (s.biUnion S)
  = sum over nonempty t subset s of
      (-1)^(card t + 1) * card (intersection over i in t of S i).
```

This matches the usual arbitrary-finite-family cardinality form. The same pinned module exposes an
indicator identity, a weighted-sum identity, and complement variants. Separately,
`Mathlib/Data/Finset/CastCard.lean` exposes `Finset.cast_card_union` for two finite sets. The probe
elaborates these interfaces and prints the reported axioms of the principal cardinality candidate
and two-set identity.

These candidates could support E1 only after exact statement identity, provenance, and trust are
checked in later phases. At intake they show usable pinned interfaces, hence provisional M3, but
they do not establish that the missing catalog formula was intended to be precisely the mathlib
declaration. No wrapper, body relocation, proof credit, or exhaustive anchor-audit claim is made.

Git history traces the candidate declaration and its proof body to mathlib commit
`d6c2c9157d71b59d98033b31423a0db08f11c4b4`, authored by Yael Dillies on 2024-11-19 as
`feat: inclusion-exclusion principle (#17957)`. This is useful formal-artifact provenance, not a
primary mathematical source or human-proof genealogy.

## Statement delta still open

Relative to the literal record, selecting the pinned finite-family candidate would add all of the
following: finite index support `s`; finite member sets `S i`; decidable equality for elements;
integer-valued equality; a powerset of index subfamilies; exclusion of the empty subfamily; a
specific nonempty-intersection operator; alternating signs; and an explicit empty-family behavior.
Those additions are standard mathematics, but they are still source-statement content absent from
the record. They require explicit source selection or reviewed normalization, not silent intake.

## First downstream gate

The statement phase must locate and review an immutable mathematical statement, or obtain an
independent scope decision approving the finite-family normalization. It must then map all binders,
finiteness assumptions, coefficient/cast choices, intersection and union conventions, conclusion,
alternate forms, and degenerate cases; elaborate the exact Lean expression; and mutation-test it.
Until then the catalog root remains `H5 / M3 / R4`, with no canonical expression or accepted
source proof.
