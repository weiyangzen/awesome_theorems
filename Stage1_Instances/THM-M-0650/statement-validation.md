# Statement validation record

Item: `S56-M-0650-STATEMENT`  
Base revision: `2414fa7f8693bbe8d5b656241466f11ec0430a5f`

## Frozen target

`Stage1Instances.THM_M_0650.TarskiVaughtTarget` fixes the nontrivial direction selected at intake.
For an arbitrary first-order language, structure, and substructure, its premise quantifies over all
finite parameter arities (including zero), bounded formulas with one final witness variable,
parameter tuples in the substructure, and ambient witnesses. It concludes `S.IsElementary`.
`tarskiVaughtTarget_iff_pinnedMathlibStatementShape` checks the direct pinned declaration shape by
definitional equality. The sole direct import is `Mathlib.ModelTheory.ElementarySubstructures`.

The repository metadata does not contain a pinpoint primary source. Therefore this node freezes the
exact modern implication selected by the accepted intake and aligned with the pinned mathlib API; it
does not claim historical source fidelity, the customary converse, or an iff.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned `.lake` environment. No update, build, clone, fetch, or dependency mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard valid: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0650` | 0 | rank 696, planned, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0650/Statement.lean` | 0 | target, checked transport, four mutations, and nullary-parameter boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0650/check_statement.py` | 0 | expression SHA-256 `33ef21b5...a5e2`; all four mutations distinguished |
| `lake env lean --version` and `lake --version` | 0 | Lean 4.29.0 at commit `98dc76e3...6740`; Lake 5.0.0-src+98dc76e |
| `sha256sum Stage1_Instances/THM-M-0650/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `76a17bc8...a6c`, `651c8acc...1d2`, and `321626c8...d81` |

The mutations remove the witness premise, replace the substructure by an arbitrary embedding, move
the conclusion inside formula/parameter scope, or exclude `n = 0`. Each elaborates but has an
explicit expression distinct from the root. `nullaryParameterBoundary` kernel-checks that the
canonical premise really specializes at `n = 0`.

This is scoped statement evidence pending master acceptance. It gives no source, proof, validation,
release, audit-completion, or theorem-completion credit.
