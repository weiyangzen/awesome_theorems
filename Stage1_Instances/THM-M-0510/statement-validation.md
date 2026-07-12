# Statement validation

Item: `S56-M-0510-STATEMENT`  
Base revision: `aa55669bb59986e08ea8a0d1d77a1e40343d8142`

## Frozen target

`Stage1Instances.THM_M_0510.HardyRamanujanAsymptoticTarget` is the exact conventional claim
selected by the accepted intake scope: the real cardinality of `Nat.Partition n` is asymptotic,
along `Filter.atTop` on naturals, to
`exp (pi * sqrt (2*n/3)) / (4*n*sqrt 3)`. The target has no hypotheses. Its two direct imports
are `Mathlib.Combinatorics.Enumerative.Partition.Basic` and
`Mathlib.Analysis.SpecialFunctions.Pow.Real`; removing either fails elaboration, while the explicit
asymptotics import proved redundant and was removed.

`target_iff_expandedTarget` kernel-checks the direct expansion. Four separately elaborated
mutations distinguish loss of the full partition asymptotic, a changed index domain, a pointwise
equality substituted for the limit, and a principal positive filter substituted for `atTop`.
`mainTerm_at_zero` checks the totalized boundary value at zero.

## Commands and results

Commands ran in this worker clone against the existing pinned Lake environment. No dependency
update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0510/Statement.lean` | 0 | exact target, expansion transport, four mutations, zero boundary, and explicit target expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0510/check_statement.py` | 0 | expression SHA-256 `9c84bc6acd929a60f87942f0ae5647b0430b9164e35249e561bccecc0cb91b41`; all four mutations distinguished |
| import-removal checks using temporary copies and `lake env lean` | 0 for the test harness | partition import removal failed at `Nat.Partition`; power import removal failed at `Real.exp`; asymptotics import removal still elaborated and the import was deleted |
| `sha256sum Stage1_Instances/THM-M-0510/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `2bdbd9...bd049`, `651c8a...b1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0510` | 0 | rank 884, planned, legacy artifacts unaccepted, theorem incomplete |

## Status boundary

This is statement-node evidence pending master acceptance. The original article's exact formula
pinpoint, assumptions/errata review, and independent source review remain open and prevent H0; the
anchor audit and every proof, trust, provenance, hermetic, and release gate also remain open. No
proof or theorem completion is claimed.
