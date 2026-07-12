# THM-M-0044 statement validation

Item: `S56-M-0044-STATEMENT`
Base revision: `7e54c0fcaf9c0e53fa7afbbeb0a36218152f932c`

## Frozen target

`Stage1Instances.THM_M_0044.SingularValueDecompositionTarget` is the closed conjunction of the
full finite rectangular SVD over `Real` and over `Complex`. Numeric index types `Fin m` and `Fin n`
make the rectangular diagonal convention explicit. The canonical diagonal has `min m n`
nonnegative real entries, is zero off equal numeric positions, and is embedded into the selected
scalar field. Both factors are square members of mathlib's unitary group, and the equality is
`A = U * Sigma * star V`.

The direct imports are `Mathlib.Analysis.Complex.Basic` and
`Mathlib.LinearAlgebra.UnitaryGroup`. No singular-values or spectral theorem module is required for
statement elaboration. The exact closed root avoids quantifying over hypothetical future `RCLike`
instances; the stronger polymorphic form is separately credited only through a checked implication.

## Commands and results

Commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean`, reused the
canonical pinned `.lake`, and performed no update, fetch, clone, or build.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0044` | 0 | rank 1084, planned, L0/rework-required, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0044/Statement.lean` | 0 | exact root, direct `Iff.rfl`, stronger-form implication, five mutations, and both empty-dimension boundary witnesses elaborated |
| `python3 ../../Stage1_Instances/THM-M-0044/check_statement.py` | 0 | expanded canonical expression SHA-256 `f9a0f27a...b1052b`; all five mutation expressions differed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum ../../Stage1_Instances/THM-M-0044/Statement.lean ../../Stage1_Instances/THM-M-0044/check_statement.py lean-toolchain lake-manifest.json` | 0 | `29f456...141c`, `770488...14e2`, `651c8a...b1d2`, `321626...2d81` |
| placeholder scan over owned Lean files | 1 | expected no-match exit; no `sorry`, `admit`, `sorryAx`, bodyless axiom, constant, opaque, or unsafe declaration |

This is statement-only evidence pending master acceptance. The inspected Axler source lead assumes
nonzero spaces and orders singular values; the frozen proposition extends the trivial empty cases
with checked witnesses and does not require ordering because the catalog's factorization claim does
not mention it. Source admission, the acceptability of this extension, independent review, and the
`THM-M-1449` duplicate decision remain open. Therefore no `H0`, proof, downstream phase, audit
completion, theorem completion, or release claim is made.
