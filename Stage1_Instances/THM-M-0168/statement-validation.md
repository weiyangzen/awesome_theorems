# Statement validation record

Item: `S56-M-0168-STATEMENT`
Base revision: `0a66013e1558a3bc4e31c9d7f64c0e8fb1dfebab`

## Frozen target

`Stage1Instances.THM_M_0168.BernsteinMinimalGraphTarget` formalizes the intake-selected analytic
version of the two-dimensional Bernstein theorem. Its domain is exactly the full product plane
`Real x Real`; `u` is `C2`; and the hypothesis is the coordinate minimal-surface equation

```text
(1 + u_y^2) u_xx - 2 u_x u_y u_xy + (1 + u_x^2) u_yy = 0.
```

The conclusion has function-local coefficients `a`, `b`, and `c` and asserts pointwise affineness.
Coordinate derivatives are Frechet derivatives evaluated on `(1, 0)` and `(0, 1)`. The exact
regularity and PDE formulation selected here matches the scoped classical entire-graph claim; a
transport from geometric minimality is a later proof obligation and is not claimed here.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0168/Statement.lean` | 0 | target and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0168/check_statement.py` | 0 | expression SHA-256 `b5cef8a8bb3b5505be6670f226315884282c53bb0040c30345f4fb0dc33254f5`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0168/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `5e7732...1a78`, `651c8a...1d2`, `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0168` | 0 | rank 665, planned, theorem incomplete |

The mutations remove the minimality hypothesis, replace the plane by a line, move the affine
coefficients outside the function binder, and strengthen the hypothesis with `u_x = 0`. They all
elaborate but have distinct explicit expressions, so none silently substitutes for the target.

This is statement-only evidence pending master acceptance. It gives no proof or theorem-completion
credit; source pinpointing, the geometric transport, and every dependent rev-5.6 node remain open.
