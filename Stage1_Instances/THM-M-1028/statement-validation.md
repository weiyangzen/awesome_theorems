# Statement validation record

Item: `S56-M-1028-STATEMENT`  
Base revision: `446447c65190dc818b074bf543171f807e9b4651`

## Frozen target

`AwesomeTheorems.Stage1.THM_M_1028.Statement` states the intake claim without
assuming either terminal property. The standard Wiener law is expressed by the
exact centered Gaussian law and mutual independence of adjacent increments on
every ordered nonnegative finite grid. The conclusion chooses a coordinatewise
modification and puts continuity and domain-relative nowhere differentiability
on the same full-measure event.

The direct imports provide calculus predicates, the real Gaussian distribution
and `HasLaw`, and indexed independence. No broad `Mathlib` import or historical
Stage1 module is used. Import-minimality beyond this narrow direct surface was
not claimed by silently relying on unstable transitive imports.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned Lake
environment. No dependency state was fetched or mutated.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1028/Statement.lean` | 0 | canonical statement and four scope mutations elaborated; canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-1028/check_statement.py` | 0 | expression SHA-256 `b2b4d22cf67e788a83c50a50a8510737e5c3a82f972be439f3c5f3d27cdfbf40`; all four mutations distinguished; pinned mathlib revision reported |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1028/Statement.lean lean-toolchain lake-manifest.json` | 0 | `ed1e047...b6dc`, `651c8ac...1d2`, and `321626c...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1028` | 0 | rank 221, planned, L0/rework-required, theorem incomplete |

## Scope guard

Expression comparison distinguishes removal of nowhere differentiability,
strengthening modification to indistinguishability, removal of increment
independence, and broadening from nonnegative to all real time. Repeated grid
times and the empty increment family are intentionally valid boundary cases;
the Gaussian variance proof is kernel checked from grid monotonicity.

This is statement-only evidence pending master acceptance. Primary-source
acceptance remains an H-axis task, and all anchor, proof, validation, and
release nodes remain open.
