# THM-M-0957 proof-phase validation

Item: `S56-M-0957-PROOF`

Date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `8714972d4cf7ae256a92b9e35032c9df1bf5745c`

## Implemented proof route

`Proof.lean` proves all thirteen frozen proof leaves: the sharp dimension,
radix nonzeroness and floor comparison, ambient fit, real-power
normalization, proxy identity and subtraction slack, reciprocal core,
linear ceiling and increment absorption, dimension slack, logarithmic
dimension loss, and inclusive-index transport. It installs the pinned
`Behrend.bound_aux` construction without weakening the historical sharp
constant.

The module then replays every frozen composer through parameter
admissibility, proxy logarithmic retention, balanced exponent control,
proxy and floored-radix asymptotics, the sharp estimate, parameter assembly,
and the root. The terminal declaration is also bound directly to
`Stage1Instances.THM_M_0957.BehrendConstructionTarget`. Thus the exact root
is kernel-closed and all 26 proof-reachable obligations have provisional
proof evidence.

This is a candidate for repo-local `M0-L` after E0 validation and
dependency-ordered master acceptance. Accepted state remains `H1/M3/R3`.
This proof worker does not claim theorem completion: source, readable,
complete trust/provenance, validation, hermetic replay, independent
verification, and release gates remain downstream.

## Commands and results

Validation reused the automation-provided pinned `.lake` artifacts read-only.
No `lake update`, `lake build`, dependency clone/fetch, network operation, or
`.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `bash Stage1_Instances/THM-M-0957/check_proof.sh` | 0 | Isolated trust-zero elaboration checked the statement, obligation tree, and exact proof; all 27 proof declarations were sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`; structural receipt checks passed. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets with ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0957` | 0 | Rank 1491; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| JSON syntax checks for the receipt and worker packet | 0 | Both structured artifacts parsed. |
| Prohibited-device scan over `Proof.lean` | 0 | No executable placeholder, bodyless declaration, unsafe/opaque/extern declaration, implementation escape, or native oracle. |
| `git diff --check -- Stage1_Instances/THM-M-0957 .stage1-worker-selftest.json` | 0 | No scoped whitespace errors. |

The worker packet proposes `[_]` only for this self-tested proof-phase
contribution. The integration lane controls acceptance, and the validation
and release nodes remain separate.
