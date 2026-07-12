# Scope map

## Included claim

- A first-order language `L`, an ambient `L`-structure `M`, and an `L`-substructure `S`.
- Formulas with one distinguished witness variable and a finite tuple of parameters from `S`.
- The witness-closure premise: an ambient witness in `M` can be replaced by a witness in `S`.
- The conclusion that `S` is elementary: all first-order formulas agree on tuples from `S` when
  interpreted in `S` and in `M`.

The intended result is the implication from witness closure to elementarity. A later source review
must decide whether the canonical human statement should be the customary iff, whose reverse
direction follows immediately from elementarity, or the nontrivial implication represented by the
pinned mathlib declaration. Intake does not silently credit the converse.

## Decisions reserved for the statement phase

The statement worker must freeze the exact universe levels, formula representation, binder order,
parameter tuple encoding, induced structure on the subtype, and direction (`implies` or `iff`). It
must also decide whether the canonical root is directly `S.IsElementary` or existence of a bundled
`L.ElementarySubstructure M`, and provide checked transports for any alternate form.

## Boundaries and exclusions

- The embedding formulation is a closely related generalization, not interchangeable root credit
  for the repository's explicit elementary-substructure gloss.
- Elementary equivalence of two structures is weaker than an identified elementary substructure
  relation and is not substituted.
- A theory-level existential-closure result, model completeness criterion, diagram argument, or
  Lowenheim-Skolem construction is outside this target.
- Restricting the criterion to quantifier-free, sentence-only, parameter-free, relational-only, or
  finite structures would broaden or weaken the source claim and is excluded.

## Formal surface map

At the pinned mathlib revision, `Mathlib.ModelTheory.ElementarySubstructures` defines
`FirstOrder.Language.Substructure.IsElementary` and proves
`FirstOrder.Language.Substructure.isElementary_of_exists`. Its premise uses
`L.BoundedFormula Empty (n + 1)`, parameter tuples `Fin n -> S`, `Fin.snoc`, and formula
realization. `Mathlib.ModelTheory.ElementaryMaps` contains the analogous embedding theorem. These
are candidate surfaces only until the dependent statement and anchor-audit phases close.
