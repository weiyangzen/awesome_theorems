# Statement validation record

Item: `S56-M-0657-STATEMENT`  
Base revision: `5b9e686366f361227feae83dad76ed1231180191`

## Frozen target

`Stage1Instances.THM_M_0657.MorleyCategoricityTarget` is the intake-selected
Morley transfer claim. It quantifies over a mathlib first-order language `L`,
a theory `T`, and source and target cardinals in one explicit universe. Language
countability is `L.card <= aleph0`; both cardinals are strictly above `aleph0`.

Mathlib's `Cardinal.Categorical` expresses uniqueness of models at a cardinal
but is vacuous when no such model exists. The local
`CategoricalWithExistence` deliberately conjoins an exact-cardinality bundled
model witness. No completeness hypothesis is silently added.
`morleyCategoricityTarget_iff_existentialSourceShape` checks the alternate
"categorical in some uncountable cardinal" binder presentation.

The sole direct import is `Mathlib.ModelTheory.Satisfiability`, the module that
defines `Cardinal.Categorical` and imports the required bundled model surface.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned Lake
environment; no dependency operation was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0657/Statement.lean` | 0 | target, checked existential transport, four mutations, and two boundary probes elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0657/check_statement.py` | 0 | expression SHA-256 `95c7d92148fe7e9375ef83729de47149f0cdecec4ce440308515ddae33442fc2`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0657/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `e70540...6131`, `651c8a...1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0657` | 0 | rank 702, planned, L0/rework-required, theorem incomplete |

## Mutation and boundary policy

The validator compares explicit elaborated expressions and rejects removal of
language countability, inclusion of the countable cardinal in the domain,
relocation of the theory binder under a uniform premise, and replacement of
the arbitrary uncountable target by `aleph0`. Kernel-checked probes confirm
that categoricity exposes a model-existence witness and that `aleph0` itself
does not satisfy the strict uncountability boundary.

This is statement-only evidence pending master acceptance. It does not prove
Morley's theorem or advance anchor-audit, obligation-tree, proof, validation,
or release nodes.
