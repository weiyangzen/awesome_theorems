# Statement validation record

Item: `S56-M-1518-STATEMENT`  
Base revision: `e02a455d09de7cf22e8c32abf4dfa3b6478a5c12`

## Frozen target

`Stage1Instances.THM_M_1518.StationaryActionEulerLagrangeTarget` is the exact
intake-selected implication over `Configuration n := Fin n -> Real`. It includes a
time-dependent Lagrangian, a nondegenerate time interval, path endpoint equalities,
`C2` hypotheses, stationarity under every `C1` endpoint-vanishing variation, and an
interior pointwise Euler-Lagrange conclusion.

The historical `S1_M_187.StatementShape` has the converse direction. It is therefore
recorded only as rejected discovery input and is neither transported nor credited.

## Commands and results

Commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean`
against the existing pinned Lake environment; no dependency state was mutated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1518/Statement.lean` | 0 | target, four mutations, zero-variation boundary, and nondegenerate-interval boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1518/check_statement.py` | 0 | expression SHA-256 `4cc15786f13f4e4ad7594012ab3e96613f5bffbf572523e8282b41139fe6979f`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1518/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `c5f702...c167`, `651c8a...1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 1546 uniform-L0 targets and execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1518` | 0 | rank 187, planned, L0/rework-required, theorem incomplete |

## Scope guard

Expression comparison rejects reversal of the implication, removal of fixed-path
endpoint hypotheses, restriction to autonomous Lagrangians, and replacement of
stationarity by unqualified global minimality. Kernel-checked boundary declarations
confirm that the zero variation is admissible and that the interval endpoints differ.

This is statement-only evidence pending master acceptance. It proves neither the
calculus-of-variations implication nor any later rev-5.6 node.
