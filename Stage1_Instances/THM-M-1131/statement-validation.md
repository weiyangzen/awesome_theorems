# Statement validation record

Item: `S56-M-1131-STATEMENT`  
Base revision: `f756a5a3b3e172050802423f4b98d5910b56dbb5`

## Frozen target

`Stage1Instances.THM_M_1131.Statement` selects the homogeneous isotropic classical form of
Fourier heat conduction on `Fin n -> Real`. It retains two logically distinct premises: the
constitutive law `q = -k grad T` and local energy balance
`rho*c*T_t = -div q + Q`. Its conclusion is `rho*c*T_t = k*Delta T + Q`.

The sole direct import is `Mathlib.Analysis.Calculus.Deriv.Basic`; removing the initially tested
`Mathlib.LinearAlgebra.StdBasis` import still elaborated, so that broader import was removed.
Gradient and divergence use coordinate evaluations of `fderiv`, the Laplacian is definitionally
`divergence gradient`, and the time derivative uses `deriv`. This node freezes a proposition only.

## Commands and results

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Lean commands ran from
`Formalizations/Lean` with the existing pinned Lake environment. No dependency was fetched,
updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1131/Statement.lean` | 0 | target and four mutations elaborated and printed |
| `python3 ../../Stage1_Instances/THM-M-1131/check_statement.py` | 0 | expression SHA-256 `01b3e91bb9da602483ca5af9d00787c8b264c6afb530c8b4b268c4c49c60ee99`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1131` | 0 | rank 336, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1131/statement.json` | 0 | structured statement artifact parsed |
| scoped forbidden-term scan of `Statement.lean` | 1 | expected no-match exit; no proof-gap declaration |
| `git diff --check -- Stage1_Instances/THM-M-1131 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator fingerprints Lean's printed elaborated expression and distinguishes reversal of the
flux sign, removal of energy balance, removal of the source, and substitution of spatially varying
conductivity. These establish structural nonidentity, not mathematical inequivalence.

The source crosswalk still lacks an independently accepted immutable primary edition and pinpoint,
so H0 remains open. The anchor audit, obligation graph, proof, hermetic validation, and independent
review also remain open. This is statement-only evidence pending master acceptance and makes no
theorem-completion claim.
