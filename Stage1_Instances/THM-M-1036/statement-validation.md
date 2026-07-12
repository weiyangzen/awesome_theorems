# Statement validation record

Item: `S56-M-1036-STATEMENT`  
Base revision: `d8e739d08e6a4c17f08c309bafac6637d21620bb`

## Frozen target

`Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget` freezes the
finite-dimensional global-Lipschitz theorem on a positive finite horizon. It
quantifies over a probability space, Brownian problem data, and an explicit
interpretation of deterministic and Ito integrals. Given the standard-integral
semantics, it concludes existence of a continuous adapted strong solution and
indistinguishability of every two solutions.

The integral interpretation is deliberately not an arbitrary hidden oracle:
the target requires `standard_time_integral` and `standard_ito_integral`. Those
propositions are semantic foundation obligations because this pinned mathlib
revision has no general Ito-integral construction. The later proof phase must
instantiate and discharge them; this statement check gives them no proof credit.

The two direct imports are listed in `statement.json`: adapted-process and
Gaussian-process APIs. Their transitive closure supplies the independence,
Bochner-integrability, and finite-coordinate norm types also used in the target.
Deletion tests show that removing either direct import makes elaboration fail.
The historical `S1_M_229.lean` imports more modules and is not imported or
credited.

## Commands and results

All commands ran in this worker clone. Lean commands ran from
`Formalizations/Lean` using the existing pinned `.lake` closure.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1036/Statement.lean` | 0 | target structures, canonical proposition, and three mutations elaborated; explicit canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-1036/check_statement.py` | 0 | expression SHA-256 `3717483261012dabe49b9787ad1336001262cbdf7791dfd1094c217298ac8954`; all three mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| direct-import deletion checks with `lake env lean` | 1 for each deletion | removing either direct import makes elaboration fail; the two-import list is deletion-minimal |
| `sha256sum Stage1_Instances/THM-M-1036/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `4942287d...91dc`, `651c8acc...1d2`, and `321626c8...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1036` | 0 | rank 229, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1036/statement.json >/dev/null` | 0 | structured statement artifact is valid JSON |
| scoped proof-gap declaration scan of `Statement.lean` and `check_statement.py` | 1 | no forbidden proof-gap declarations found; 1 is ripgrep's no-match exit |
| `git diff --check -- Stage1_Instances/THM-M-1036 .stage1-worker-selftest.json` | 0 | no scoped whitespace errors |

## Mutation boundary

The validator serializes explicit elaborated expressions and distinguishes:

- deletion of the uniqueness conclusion;
- fixed-time almost-everywhere equality in place of process indistinguishability;
- a changed horizon premise/binder shape.

This is statement-only evidence pending master acceptance. Human-source H0
remains open because a primary-copy page/theorem/errata crosswalk and independent
review are absent. The statement is not an SDE proof, an Ito-integral
implementation, or theorem-completion evidence.
