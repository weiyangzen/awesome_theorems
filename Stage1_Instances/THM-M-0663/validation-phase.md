# THM-M-0663 validation-phase result

Item `S56-M-0663-VALIDATION` was run against base revision
`bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad` (tree
`ca999baf360c6ce2440bbc2c01aeb8d519269a90`). Validation added no root proof
content. It re-elaborated copied `Statement.lean`, `ObligationTree.lean`, and
`Proof.lean` sources in a fresh temporary directory, then checked a separately
written reconstruction that imports only `Statement`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement boundary, conditional identity, both proof-phase declarations, and both same-worker differential declarations elaborate. |
| Placeholder/unsafe/oracle hygiene | pass in inspected modules | Comment-aware scans found no `sorry`, `admit`, `sorryAx`, local `axiom`, `constant`, `opaque`, `unsafe`, `extern`, `implemented_by`, or `native_decide` construct. This is additional defense, not a complete transitive parser audit. |
| Axiom observation | provisional pass | The four subsingleton/empty declarations and conditional identity report exactly `propext`, `Classical.choice`, and `Quot.sound`. A complete accepted foundation/TCB profile remains open. |
| Local provenance and pins | partial pass | Frozen hashes, denominator, toolchain/manifest pins, and the clean pinned mathlib revision agree. No `proof-receipt.json`, complete transitive declaration/import closure, or terminal-body packet exists. |
| Proof dependency | fail closed | `S56-M-0663-PROOF` is only `[_]` and has no master acceptance receipt. The target-local DAG remains open. |
| Exact frozen node identity | fail closed | `M0663-B-DEGENERATE` also requires an exhaustive nondegenerate branch split. Its planned fingerprint and `emptyDomainPartition` formal target do not bind the new declarations, so no whole-obligation closure is credited. |
| Exact root kernel closure | fail | `OMinimalMonotonicity` has no proof body. `root_of_partition_package` only returns an exact root supplied as a premise and earns no proof credit. |
| Hermetic release replay | fail closed | Lean ran with a fixed locale/timezone and `bubblewrap --unshare-net`, but reused the shared warm `.lake` symlink; it was not a clean-checkout, empty-cache cold build or offline restoration, and has no complete TCB/SBOM archive. |
| Independent verification | fail closed | `Validation.lean` is separately written but ran under the same identity, checkout, kernel, and cache. There is no distinct signed runner or independently implemented release verifier. |

The first dependency gate failure is
`dependency.S56-M-0663-PROOF.master_acceptance`; the first substantive proof
failure is `proof.node_exact_identity_and_root_kernel_closure`. The frozen
obligation graph reports the root as open `M3`, with domain normalization,
local continuity, local order, finiteness, source, and foundation in its first
open cut. The accepted instance vector remains `[H3, M4, R4]` with no state
promotion. `audit_complete=false` and `theorem_complete=false`.

## Commands and results

Commands ran on 2026-07-13 UTC (2026-07-14 Asia/Shanghai). Lean elaboration
ran under `bubblewrap --unshare-net`. No command ran
`lake update`, `lake build`, dependency clone/fetch, or a network operation,
and no command intentionally modified `.lake`.

```text
$ python3 -B Stage1_Instances/THM-M-0663/check_validation.py
exit 0; exact statement boundary, conditional identity, proof declarations,
and same-worker direct reconstruction replayed; axiom observation, hygiene,
frozen hashes, denominator, pins, and clean mathlib passed; proof receipt,
whole-node identity, root, complete trust, hermetic, and independent gates
reported fail-closed

$ python3 Docs/tools/check_stage1_standard.py
exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

$ python3 scripts/stage1_target.py check
exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required

$ python3 scripts/stage1_target.py show THM-M-0663
exit 0; rank 707, planned lifecycle, theorem_complete=false

$ python3 -B Stage1_Instances/THM-M-0663/check_obligation_tree.py
exit 0; 14 obligations and 36 typed edges passed; root remains open M3

$ python3 -B Stage1_Instances/THM-M-0663/check_anchor_audit.py
exit 0; exact target identity and bounded negative anchor audit passed

$ python3 -B Stage1_Instances/THM-M-0663/check_statement.py
exit 0; frozen statement fragments and four mutations passed

$ git diff --check -- Stage1_Instances/THM-M-0663 .stage1-worker-selftest.json
exit 0; no whitespace errors
```

## Retry condition

First bind a complete exact `M0663-B-DEGENERATE` statement, composition, and
receipt to all of its required semantics, then obtain dependency-ordered master
acceptance. Root proof work must close the remaining o-minimal monotonicity
obligations. Release validation additionally requires immutable clean inputs,
empty caches, network-denied offline restoration, complete trust/provenance and
SBOM evidence, and a distinct signed independently provisioned verifier.
