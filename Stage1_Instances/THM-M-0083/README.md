# THM-M-0083 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the representable-functor
theorem. Historical `S1-M-139` material is discovery input only and supplies no
accepted statement or proof credit.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A presheaf `F : Cᵒᵖ ⥤ Type w` is representable iff it has an object `X` and universal element `x` inducing bijections `(Y ⟶ X) ≃ F.obj (op Y)` for every `Y` | This is the provisional interpretation of the terse source phrase “conditions for a functor to be representable”; exact elaboration is deferred |
| Domains | Locally small Lean category `C`, universe-polymorphic Type-valued presheaf, all test objects and morphisms | Universe constraints and binder order must be frozen by the statement phase |
| Forward direction | A universal element constructs a representation | No proof credit is inherited from the legacy wrapper |
| Reverse direction | A representation yields a universal element and bijections | No proof credit is inherited from mathlib names found during intake |
| Consequences | Representing objects are unique up to isomorphism; Yoneda and adjoint bridges | Context only, excluded from the exact root unless a later source audit changes scope |
| Homological/AFT branches | Legacy imports concerning derived functors, exact sequences, and adjoint functor theorems | Excluded from the root: they are applications or stronger existence criteria, not the universal-element characterization |
| Foundations | Lean 4 kernel with pinned mathlib; ordinary category-theory foundations and permitted classical principles | Exact toolchain, dependency, axiom, TCB, and computation profiles remain open |

The canonical human claim and provisional formal target are structured in
`intake.json`. Source correspondence and ambiguities are recorded in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate: there is no accepted
normalized expression hash, environment fingerprint, checked transport set, or
mutation report. This intake is self-tested as an intake artifact only. It does
not establish theorem completion or accept the later statement, proof, or
release phases.

## Validation

The exact commands and results are in `validation.md`.
