# Statement validation record

Item: `S56-M-1058-STATEMENT`  
Base revision: `8509654fd1347228b71158b61f9f700360aa1691`

## Frozen target

`Stage1Instances.THM_M_1058.LargeDeviationPrinciple` is the intake-selected full
open/closed-set LDP property for a supplied sequence of probability measures. The data fixes a
positive speed tending to infinity and a nonnegative lower-semicontinuous `EReal` rate. The scaled
log probability uses `ENNReal.log` directly, rather than the legacy module's caller-supplied
abstract logarithm and scaled-log field. Four direct imports are needed for probability measures,
liminf/limsup, lower semicontinuity, and the extended logarithm.

`PinnedCandidateSourceShape` directly expands the formula, and
`largeDeviationPrinciple_iff_pinnedCandidateSourceShape` is its kernel-checked transport. This is
a definition/property boundary, not an assertion that arbitrary probability measures obey an LDP.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned `.lake` artifacts. No
dependency update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1058/Statement.lean` | 0 | target, direct-expansion iff, and four mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1058/check_statement.py` | 0 | expression SHA-256 `60a04b...a33`; removed-hypothesis, changed-domain, binder-scope, and weak-LDP boundary mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1058/Statement.lean lean-toolchain lake-manifest.json` | 0 | `91a805...d5c`, `651c8a...1d2`, `321626...d81` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1058` | 0 | rank 250, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1058/statement.json >/dev/null` | 0 | statement receipt is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1058` | 0 | no whitespace errors |

## Mutation policy

The validator compares the explicit elaborator output and rejects removal of speed divergence,
specialization of the arbitrary state space to `Real`, relocation of the open branch beneath the
closed-set binder, and substitution of compact sets for closed sets. The last mutation is the weak
LDP boundary. Goodness of the rate function remains excluded.

This is self-tested statement evidence pending master acceptance. It does not advance anchor-audit,
obligation-tree, proof, validation, or release nodes and does not claim theorem completion.
