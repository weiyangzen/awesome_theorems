# THM-M-0707 validation-phase result

Item: `S56-M-0707-VALIDATION`  
Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`  
Validation time: `2026-07-12T16:22:19+08:00`

The narrow validator re-elaborated the exact proof-phase root and a separately
written reconstruction that imports only `Statement`. The reconstruction does
not import `Proof` or `ObligationTree`. Both routes restrict a hypothetical
arbitrary-code/arbitrary-input decider to input zero and apply the pinned
`ComputablePred.halting_problem 0`; thus validation reaches the exact frozen
root rather than a fixed-input substitute.

Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. Source scans
found no `sorry`, `admit`, `sorryAx`, local `axiom`/`constant`, or `unsafe`
declaration. The proof receipt, frozen statement, registry, graphs, manifest,
clean mathlib revision, and pinned halting source hashes agree.

## Commands and results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0707` | 0 | Rank 748, planned, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0707/check_obligation_tree.py` | 0 | 12 obligations and 34 typed edges passed; acceptance remains open. |
| `python3 Stage1_Instances/THM-M-0707/check_statement.py` | 0 | Exact expression hash `9eea217b...e46b`; all four structural mutations killed. |
| `python3 Stage1_Instances/THM-M-0707/check_validation.py` | 0 | Exact primary and Statement-only reconstructions elaborated; trust, hygiene, hashes, source, and pin checks passed. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib status --porcelain` | 0 | Empty output; pinned dependency worktree clean. |

The validator used temporary local OLean output and deleted it. It performed no
update, build, clone, fetch, network operation, or `.lake` mutation.

## Gate decisions

| Gate | Decision | Boundary |
|---|---|---|
| Narrow exact-root kernel replay | pass | Warm pinned-cache worker evidence only. |
| Differential reconstruction | pass | Separately written, but same worker and cache. |
| Placeholder/unsafe hygiene | pass | All three checked Lean modules are clean. |
| Trust observation | provisional pass | Observed axiom set is exactly the allowed profile above; complete transitive TCB acceptance is open. |
| Local provenance/freshness | pass | Local hashes, clean pinned mathlib source, manifest, and proof receipt agree. |
| Hermetic cold offline replay | fail closed | Shared warm `.lake`; no clean empty-cache rebuild, restorable archive, full TCB/SBOM, or deterministic bundle. |
| Independent verification | fail closed | No distinct identity, independently provisioned checkout/cache, or second signed attestation. |

The first failed gate is `S56-10.6-HERMETIC-COLD-BUILD`; the independent-runner
gate also remains open. `M0707-X-SOURCE`, `M0707-X-FOUNDATION`, and
`M0707-X-PROVENANCE` remain the frozen release cut set. This receipt claims
neither audit completion nor theorem completion, release, accepted state, or
master acceptance.
