# Statement validation record

Item: `S56-M-0088-STATEMENT`  
Base revision: `c2687431b1d86bac7bd509c9abbfdc1e763c060c`

## Frozen target

`Stage1Instances.THM_M_0088.YonedaEmbeddingTarget` is the exact intake-selected data type
`(yoneda (C := C)).FullyFaithful`, for `C : Type u` with `[Category.{v} C]`. Its single direct
import is `Mathlib.CategoryTheory.Yoneda`, the pinned defining module for both `yoneda` and its
fully-faithful data. The target retains the contravariant presheaf codomain `Cᵒᵖ ⟶ Type v`.

The checked `Iff.rfl` transport shows that the historical `Nonempty FullyFaithful` proposition is
exactly existence of the selected data-valued target. No inhabitant is declared here: the statement
node neither imports the legacy wrapper nor applies `Yoneda.fullyFaithful` as proof evidence.

## Commands and results

Lean commands ran from `Formalizations/Lean` with the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0088/Statement.lean` | 0 | exact target and definitional transports elaborated; explicit universe/type output and pinned candidate type printed |
| `python3 ../../Stage1_Instances/THM-M-0088/check_statement.py` | 0 | expression SHA-256 `09b7265949046c6554d511b26406306ca81f0d19004a54e959f9fac4abc55519`; faithful-only, co-Yoneda, and universe-raised mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-0088/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `7149fe...a6b`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0088` | 0 | rank 137, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Boundary policy

The category may be empty; no chosen objects or morphisms and no extra algebraic structure are
assumed. The validator distinguishes removal of fullness, reversal to co-Yoneda, and changing the
codomain universe. Essential surjectivity is outside the claim.

This is statement-only evidence pending master acceptance. It does not advance anchor-audit,
obligation-tree, proof, validation, or release nodes and does not claim theorem completion.
