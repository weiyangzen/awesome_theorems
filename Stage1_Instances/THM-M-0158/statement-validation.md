# Statement validation record

Item: `S56-M-0158-STATEMENT`  
Base revision: `b5a452fcaf03fdb99da11e1749d1f393684d8fe3`

## Frozen target

`Stage1Instances.THM_M_0158.WeingartenEquationsTarget` formalizes the intake-selected local
Weingarten formula. `U` is an open subset of the Euclidean parameter plane, `x` is `C2`, `N` is a
`C1` unit normal orthogonal to both coordinate tangents, and the Gram matrix at the selected point
is nonsingular. Partials use `fderivWithin`; `II i j = <partial_j(partial_i x), N>`. The conclusion
fixes the column convention `N_i = sum_j (-(I^-1 * II)) j i x_j`.

## Commands and results

All Lean commands ran from `Formalizations/Lean` against the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0158/Statement.lean` | 0 | target and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0158/check_statement.py` | 0 | expression SHA-256 `62594b8173c0478a49cafb93c7f668b9a8a9302e6f2b194ce7d4e6bd0668eb9a`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0158/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes `1435d5...bc3`, `651c8a...1d2`, `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0158` | 0 | rank 657, planned, theorem incomplete |

The structural mutations remove pointwise regularity, replace the open local domain with the whole
plane, strengthen regularity to every point, and permit evaluation outside `U`. They elaborate but
have distinct explicit expressions, so none can silently substitute for the canonical target.

This is statement-only evidence pending master acceptance. It gives no proof or theorem-completion
credit; source pinpointing and all dependent rev-5.6 nodes remain open.
