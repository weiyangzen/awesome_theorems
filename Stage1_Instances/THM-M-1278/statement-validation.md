# Statement validation record

Item: `S56-M-1278-STATEMENT`  
Base revision: `ad0567008a38fc8c39deda009ab34e4ca9910f46`

## Frozen target

`Stage1Instances.THM_M_1278.OnofriInequality` is the normalized sharp Onofri inequality for a
smooth real-valued function on the standard round unit two-sphere. `Sphere2` is the radius-one
metric sphere in `EuclideanSpace Real (Fin 3)`; `sphereArea` is its two-dimensional Hausdorff
measure; and `dirichletEnergy` integrates the squared norm of the ambient gradient projected to
the tangent plane. Smooth functions are concretely represented by global smooth ambient
extensions. This sufficient representation avoids assuming the desired inequality and makes all
analytic terms kernel-visible.

The publisher page for Onofri's DOI `10.1007/BF01212171` was inspected. Its abstract explicitly
states the constrained positivity form for `C-infinity` functions on the two-dimensional sphere.
The normalized logarithmic target is the algebraic reformulation recorded in
`source-statement-crosswalk.md`. Full article-page, normalization, and errata review remains an H
gate and is not overstated here.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` with the
existing pinned Lake environment; no dependency was fetched or updated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1278/Statement.lean` | 0 | exact target, sphere/measure/gradient definitions, and two mutations elaborated; explicit declarations printed |
| `python3 ../../Stage1_Instances/THM-M-1278/check_statement.py` | 0 | canonical expression SHA-256 `a267837c...1fdb`; zero-mean-only and coefficient mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1278/Statement.lean lean-toolchain lake-manifest.json` | 0 | `efd71349...d7f6`, `651c8acc...b1d2`, `321626c8...d81`; recorded in `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1278` | 0 | rank 449, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1278/statement.json` | 0 | structured statement artifact is valid JSON |
| scoped forbidden-term scan | 1 | no `sorry`, `axiom`, or proof-gap declaration; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-1278 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is statement-only evidence pending master acceptance. It does not prove the Onofri inequality
or advance anchor-audit, obligation-tree, proof, validation, or release nodes. Source fidelity H0,
the exact area theorem for `sphereArea`, anchor provenance, theorem kernel closure, and independent
validation remain open.
