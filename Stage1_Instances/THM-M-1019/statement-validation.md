# Statement validation record

Item: `S56-M-1019-STATEMENT`  
Base revision: `f552b1fbe91904b0d46dad9e5e29e9075fc93c1e`

## Frozen target

`Stage1Instances.THM_M_1019.Statement` states that two Borel probability measures on `Real` are
equal when their mathlib characteristic functions agree. The checked theorem
`statement_iff_integralForm` connects that API-level expression to pointwise equality of the
integrals `integral (fun x => exp (t * x * I))`. The sign and factor order match mathlib's
`charFun_apply_real` exactly.

The sole direct import is `Mathlib.MeasureTheory.Measure.CharacteristicFunction.Basic`, the pinned
module that defines `charFun`, proves its real integral expansion, and provides the relevant measure
API. This node freezes a statement and a transport, not a proof of the root.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned Lake environment; no dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1019/Statement.lean` | 0 | canonical target, integral form, checked equivalence, and four mutations elaborated and printed |
| `python3 ../../Stage1_Instances/THM-M-1019/check_statement.py` | 0 | expression SHA-256 `9e3e6807774912fde69809f88fb4928406a4241c5c3df6ff4bbacfe0c92e3d69`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1019` | 0 | rank 495, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1019/statement.json` | 0 | structured statement artifact is valid JSON |
| scoped forbidden-term scan | 1 | expected no-match exit; no forbidden proof escape occurs in executable statement/validator content |
| `git diff --check -- Stage1_Instances/THM-M-1019 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator structurally distinguishes removal of the probability hypotheses, changing the
domain to `Complex`, restricting the frequency binder to nonnegative reals, and excluding the
Dirac-zero boundary case. Structural nonidentity does not assert mathematical non-equivalence; the
tests prevent silent substitution of the frozen syntax and scope.

The random-variable encoding remains uncredited because it needs a separate checked pushforward
transport. Primary-source edition/page review remains open on the H axis, as do anchor audit,
obligation graphs, proof, hermetic replay, and independent review. This is statement-only evidence
pending master acceptance and makes no theorem-completion claim.
