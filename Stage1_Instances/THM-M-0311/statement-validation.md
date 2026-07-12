# Statement validation record

Item: `S56-M-0311-STATEMENT`  
Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`

## Frozen target

`Stage1Instances.THM_M_0311.RieszFischerTarget` freezes the repository's explicit gloss,
"completeness of L2 spaces," for both standard scalar fields. For every measurable carrier and
every measure, it asserts `CompleteSpace` for the real and complex `MeasureTheory.Lp` quotient at
exponent `2`. This retains zero, empty, and infinite-measure cases and does not add sigma-finiteness.

The historical Fourier-coefficient realization version of Riesz-Fischer is not silently identified
with this target. A pinpoint source bridge remains human-source work for the anchor-audit phase.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` environment. No
dependency update, fetch, clone, or build was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0311/Statement.lean` | 0 | exact target, checked direct encoding, four structural mutations, and zero/empty/infinite boundary fixtures elaborated; fully explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0311/check_statement.py` | 0 | expression SHA-256 `38cbb055cfb3734633dad981d0bd36dfb2dd89720a64e09659a1c19aae4c3d84`; all four mutations distinguished; pinned mathlib revision reported |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0311/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `e3be486d...695cb`, `651c8acc...b1d2`, and `321626c8...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0311` | 0 | rank 813, planned, legacy artifacts unaccepted, theorem incomplete |

The mutations remove one scalar case, restrict the carrier, move the measure from universal to
existential scope, and add an excluded finite-measure premise. They elaborate but serialize to
expressions distinct from the canonical target, so none can substitute for it.

This is self-tested statement-only evidence pending master acceptance. It gives no proof,
anchor-audit, dependent-node, audit-completion, or theorem-completion credit.
