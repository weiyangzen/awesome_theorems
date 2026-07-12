# THM-M-0312 release decision

Item: `S56-M-0312-RELEASE`  
Base revision: `bd0d227173ac95971603f633607751754850337e`  
Decision date: `2026-07-12` (`Asia/Shanghai`)

## Exact verdict

The release is **blocked**. The lifecycle remains `planned`, the accepted root vector remains
`[H1, M3, R3]`, and both `audit_complete` and `theorem_complete` remain false. No receipt is
accepted and no `AUDIT-Z`, `THEOREM-Z`, release, or master-acceptance claim is made.

The first failure is dependency acceptance: `S56-M-0312-VALIDATION` is only `[_]` provisional
worker evidence. Its useful result is narrow and real: the exact root and a differential
reconstruction elaborate in pinned Lean with only `propext`, `Classical.choice`, and `Quot.sound`
observed. It used the same worker and shared warm cache, so it is not release-grade or independent.

The next failure is authoritative state reconciliation. The frozen graph still exposes candidate
proof interfaces and the open foundation/provenance/source nodes `M0312-S-FOUNDATION`,
`M0312-X-PROVENANCE`, and `M0312-X-SOURCE`. Only the master can reconcile accepted M state. Primary
source `H0`, independently reviewed `R0`, cold offline replay, supply-chain closure, independent
attestations and verifier, CI mutations, and a deterministic release bundle are absent.

## Commands and results

All commands ran from the repository root. No dependency update, build, clone, fetch, or `.lake`
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-0312` | 0 | Rank 814, planned, L0/rework-required, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0312/check_validation.py` | 0 | Narrow kernel, axiom, hash, pin, and differential checks passed; release gates failed closed. |
| `python3 Stage1_Instances/THM-M-0312/check_release.py` | 0 | Blocked verdict, unaccepted dependency, unchanged state, false terminal booleans, hashes, and cut set agree. |
| `python3 -m json.tool Stage1_Instances/THM-M-0312/release-decision.json` | 0 | Valid JSON. |
| Placeholder scan over `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `Validation.lean` | 1 | Expected no-match result; no prohibited placeholder, added axiom, or unsafe declaration. |
| `git diff --check -- Stage1_Instances/THM-M-0312 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

## Retry boundary

The integration lane must accept the phase dependency and reconcile the structured graph without
overstating the warm-cache evidence. Independent source/readability review and a separately
provisioned release lane must close the remaining trust, hermetic, supply-chain, verifier, CI, and
bundle gates before theorem completion can truthfully be reconsidered.
