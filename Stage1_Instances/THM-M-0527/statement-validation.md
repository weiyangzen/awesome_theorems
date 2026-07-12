# Statement validation record

Item: `S56-M-0527-STATEMENT`

Base revision: `5c1dd64c0dd1631649e94682e2f0322535c44103`. Commands ran in the worker
clone on 2026-07-12 against the existing pinned `.lake` environment. No update, fetch, build, or
dependency mutation was performed.

## Frozen target

`Stage1Instances.THM_M_0527.CoveringSpaceClassificationTarget` is the pointed classification from
the accepted intake scope. It quantifies over a based path-connected and locally path-connected
space, assumes the explicitly defined semilocal simple-connectedness condition, and fixes the
forward assignment as the range of the induced fundamental-group homomorphism. Surjectivity gives
a cover for every subgroup; equality of assigned subgroups exactly when covers are pointed-
isomorphic supplies the quotient-free injectivity criterion.

The sole direct import is `Mathlib.Topology.Homotopy.Lifting`. It is the narrow pinned module that
exposes covering maps and the fundamental-group map used by the target. The unpointed conjugacy
form remains an alternate encoding and receives no statement-gate credit here.

## Commands and results

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0527` | 0 | rank 584; planned; hard-statement-first lane; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0527/Statement.lean)` | 0 | target, definitions, and three mutations elaborated; explicit canonical expression printed |
| `(cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0527/check_statement.py)` | 0 | expression SHA-256 `4c7a7d4c...625f55d`; all three mutations distinguished |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0527/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `00d230...1327`, `651c8a...b1d2`, `321626...2d81` |
| `python3 -m json.tool Stage1_Instances/THM-M-0527/statement.json >/dev/null` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0527` | 0 | no whitespace errors |

The mutation validator separately elaborates removal of semilocal simple-connectedness, removal of
local path connectedness, and weakening to the existence half alone, then confirms that none has
the canonical elaborated expression. This is statement-only evidence pending master acceptance;
it does not claim a proof or theorem completion.
