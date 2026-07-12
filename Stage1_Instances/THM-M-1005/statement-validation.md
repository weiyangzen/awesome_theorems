# Statement validation record

Item: `S56-M-1005-STATEMENT`  
Base revision: `656a1be3548d492354ef99a755ef0bbcab9bd22b`

## Frozen target

`Stage1Instances.THM_M_1005.Statement` is the strong finite-horizon `L^p` Doob inequality selected
by the target gloss "moment estimate for a martingale maximum": for a real-valued discrete-time
martingale and `1 < p < infinity`, the `eLpNorm` of the inclusive running absolute maximum through
`n` is bounded by `p / (p - 1)` times the `eLpNorm` at time `n`.

The direct import is `Mathlib.Probability.Martingale.OptionalStopping`. It is minimal among the
pinned modules exercised here: it provides the martingale/filtration API and transitively the
`eLpNorm` notation needed by the proposition. This node freezes a statement, not a proof. In
particular, the pinned module's proved weak maximal inequality for nonnegative submartingales is a
different proposition and receives no completion credit here.

## Commands and results

All commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned Lake environment; no dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1005/Statement.lean` | 0 | canonical target and four structural mutations elaborated and printed |
| `python3 ../../Stage1_Instances/THM-M-1005/check_statement.py` | 0 | expression SHA-256 `32343e66034f94d4afabc10f4d15cbae77daf650c757023a2142aafba50366e5`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1005` | 0 | rank 285, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1005/statement.json` | 0 | structured statement artifact is valid JSON |
| scoped forbidden-term scan | 1 | expected no-match exit; no `sorry`, `admit`, `axiom`, or `sorryAx` in executable statement/validator content |
| `git diff --check -- Stage1_Instances/THM-M-1005 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator fingerprints Lean's printed elaborated expression and distinguishes replacing the
strong result by a weak tail bound, changing the process class, changing the inclusive horizon,
and admitting `p = 1`. These checks establish structural nonidentity; later mathematical
transports require their own checked proofs.

Exact primary-source edition/theorem/page and errata review remains open on the H axis, as do the
anchor audit, obligation graph, proof, hermetic replay, and independent review. This is
statement-only evidence pending master acceptance and makes no theorem-completion claim.
