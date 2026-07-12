# Statement validation record

Item: `S56-M-1200-STATEMENT`  
Base revision: `bffb5c63a3a8b89fc36a28a72eed61be8fc4d16a`

## Frozen target

`Stage1Instances.THM_M_1200.RankineHugoniotTarget` freezes the scalar, one-dimensional target
selected by intake. The interface is the straight line `x = s*t`; the weak defect is the jump
coefficient `f uR - f uL - s*(uR-uL)` paired with the trace of every smooth compactly supported
spacetime test function. Its vanishing is equivalent to the standard Rankine-Hugoniot equality.
The checked transport rewrites the equality as continuity of `f u - s*u` across the interface.

No regularity premise on `f` is required for this reduced constant-state interface defect because
only `f uL` and `f uR` occur. Deriving this reduced defect from the distributional derivative of a
piecewise-constant state belongs to the later proof architecture and receives no credit here.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned environment. No dependency
update, fetch, build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1200/Statement.lean` | 0 | target, defect definitions, checked moving-frame transport, four mutations, and two boundary lemmas elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-1200/check_statement.py` | 0 | expression SHA-256 `b77d79ed6acc61642c8288a004f1023d65a71367415ac90fd6a6c5e8af77ca93`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1200/Statement.lean lean-toolchain lake-manifest.json` | 0 | `8e1650...5ee7`, `651c8a...b1d2`, and `321626...2d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1200` | 0 | rank 394, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1200 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The mutations remove the reverse implication, force a stationary interface, exclude equal states,
or change the frozen binder order. The boundary lemmas kernel-check that equal states have zero jump
coefficient and that the defect depends only on the test-function trace along the interface.

This is statement-only evidence pending master acceptance. Source audit, anchor audit, obligation
tree, proof, full validation, release, and theorem completion remain open.
