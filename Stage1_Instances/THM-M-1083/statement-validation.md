# Statement validation record

Item: `S56-M-1083-STATEMENT`  
Base revision: `7c40b39aac30d12a21a2ca13ebe9406d4d57b383`

## Frozen target

`Stage1Instances.THM_M_1083.Statement` is the real-valued compact-interval
Kolmogorov-Chentsov theorem frozen by intake. The interval is an intrinsic `Set.Icc` subtype;
expectations are `lintegral`s of extended-distance powers; modification means fixed-time
almost-everywhere equality; and the conclusion quantifies over every strictly subcritical positive
`NNReal` exponent, allowing its almost-everywhere event and finite Holder constant to depend on the
exponent.

The direct imports are the minimal pinned feature modules used by this target: the Kolmogorov
process module supplies the increment-moment vocabulary, the probability typeclass module supplies
the probability-space condition, and the Holder module supplies `HolderWith`. This node declares
and elaborates a proposition only. It does not assert the Kolmogorov-Chentsov proof.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean` against its existing
pinned Lake environment. No dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1083/Statement.lean` | 0 | canonical target and four structural mutations elaborated and printed |
| `python3 ../../Stage1_Instances/THM-M-1083/check_statement.py` | 0 | expression SHA-256 `fb7209158513f98f9692a12449560573c5009e1a2366ed34eb8e61f9cae7c58a`; all mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1083` | 0 | rank 525, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1083/statement.json` | 0 | structured statement artifact is valid JSON |
| scoped forbidden-term scan | 1 | expected no-match exit; no prohibited proof-gap declaration occurs in executable statement/validator content |
| `git diff --check -- Stage1_Instances/THM-M-1083 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator fingerprints Lean's printed elaborated expression and distinguishes the excluded
critical exponent, a continuity-only weakening, simultaneous rather than fixed-time modification,
and deletion of the dimension-one `+ 1` in the increment power. These are structural nonidentity
checks, not proofs about transports between propositions.

Primary-source pinpoint and approval remain open on the human axis. Anchor audit, obligation graph,
proof, trust closure, hermetic replay, and independent validation also remain open. This is
statement-only evidence pending master acceptance and makes no theorem-completion claim.
