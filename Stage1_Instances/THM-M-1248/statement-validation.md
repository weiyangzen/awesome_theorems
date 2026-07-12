# Statement validation record

Item: `S56-M-1248-STATEMENT`  
Base revision: `c370639c4481be6bdcec40b9aa3553046d6f7572`

## Frozen target

`Stage1Instances.THM_M_1248.CaffarelliKohnNirenbergTarget` transcribes the sufficiency direction of
the unnumbered theorem on pages 259-260 of the primary paper. `AdmissibleParameters` contains
equations (1.1)-(1.3), dimensional balance (1.5), and both conditional restrictions culminating in
(1.7). The estimate is (1.4), for `ContDiff Real top` functions of compact support.

The source permits `r > 0`, including `r < 1`, so the weighted quantities use explicit Lebesgue
integrals and real powers rather than a normed `Lp` space. The operator norm of `fderiv` represents
the gradient norm. The separate necessity direction and uniform boundedness of `C` on compact
parameter sets are not part of the intake-selected existence estimate and receive no credit here.

The primary source snapshot was downloaded from NUMDAM as DjVu and has SHA-256
`7fe625609501f22377d92977573992ef2863156edd50d4dc9ea644e6d3c86022`.

## Commands and results

Lean commands ran from `Formalizations/Lean` using the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1248/Statement.lean` | 0 | target, parameter predicate, weighted quantities, and four mutations elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1248/check_statement.py` | 0 | expression SHA-256 `f6a658...48d5b`; all four structural mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1248/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `e3e257...3c00`, `651c8a...b1d2`, and `321626...d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository rev-5.6 assurance structure accepted |
| `python3 scripts/stage1_target.py check` | 0 | ordered manifest accepted with 1546 unique uniform-L0 targets |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | rank 428, planned, L0/rework-required, theorem incomplete |

This is statement-only evidence pending master acceptance. It does not advance anchor audit, proof,
validation, release, or theorem completion.
