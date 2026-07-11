# THM-M-0419 statement receipt

## Frozen target

`Statement.lean` freezes the exact containment form of Kronecker-Weber. For every carrier `K` in
universe `uK`, the ordered context is `[Field K]`, `[Algebra ℚ K]`, `[NumberField K]`, and
`[IsAbelianGalois ℚ K]`. The conclusion provides `n : ℕ`, proves `n ≠ 0`, fixes mathlib's
splitting-field algebra structure using `CyclotomicField.algebraBase`, and provides a nonempty
`ℚ`-algebra homomorphism from `K` into `CyclotomicField n ℚ`.

The closed `Statement` quantifies over all such presentations. `statement_iff` is a kernel-checked
expansion of its complete binder list and conclusion. An algebra homomorphism from a field is
injective, so this is the presentation-level containment claim rather than a weakened map-existence
claim. This phase does not credit an equivalence with every possible subfield presentation; that
transport remains outside the statement receipt.

## Imports and environment

The sole direct import is `Mathlib.NumberTheory.NumberField.Cyclotomic.Basic`. A negative probe with
only `Mathlib.FieldTheory.Galois.Abelian` fails because `CyclotomicField` is unknown. The selected
cyclotomic module already exports `IsAbelianGalois`, `NumberField`, and the cyclotomic API, so a
second direct import is unnecessary.

Lean is pinned at `4.29.0` (`98dc76e3c0a9b856c9b98726b713fb04fab16740`) and mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. `statement.json` records hashes of the source,
elaboration output, toolchain files, manifest, Lake file, and the resulting environment
fingerprint. No dependency was fetched or changed.

## Mutation certificate

All four required negative fixtures fail under the pinned elaborator:

| Fixture | Mutation | Expected diagnostic |
|---|---|---|
| `mutations/RemovedHypothesis.lean` | remove `[Field K]` | cannot synthesize `Field K` / `Semiring K` |
| `mutations/ChangedDomain.lean` | replace rational base by `ℤ` | cannot synthesize `Field ℤ` |
| `mutations/ChangedBinderScope.lean` | use `n` before its existential binder | unknown identifier `n` |
| `mutations/BoundaryZero.lean` | equate `n = 0` with `n ≠ 0` | `rfl` fails |

These are compile-fail fixtures, not proof files. They contain no admitted declaration and are
successful only when `lake env lean` exits nonzero with the recorded diagnostic.

## Status boundary

This is self-tested statement-phase evidence pending master acceptance. It establishes exact target
elaboration and the specified mutations only. It does not prove Kronecker-Weber, accept a human
source audit, freeze the obligation graph, or satisfy any proof, validation, or release gate.
