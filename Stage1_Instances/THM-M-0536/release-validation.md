# THM-M-0536 Release Decision Handoff

## Exact verdict

`S56-M-0536-RELEASE` is **blocked**. The lifecycle remains `planned`, the accepted root vector
remains `[H1, M4, R4]`, `audit_complete=false`, and `theorem_complete=false`. There are no accepted
receipt IDs and no theorem-completion promotion.

The first failed gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the validation prerequisite is `[_]`
worker evidence with `support_state=provisional_worker_selftest`, not a master-accepted dependency.
The next theorem-release gate is `S56-10.6-HERMETIC-COLD-BUILD`, because the successful local replay
used the canonical pinned warm dependency cache rather than an empty-cache offline build.

## Reconciliation

The proof and validation receipts agree that the exact frozen declaration
`Stage1.THM_M_0536.homotopyInvariance` kernel-checks locally, has a two-sided checked composition,
contains no placeholder, and reports exactly `propext`, `Classical.choice`, and `Quot.sound`. This is
provisional `M0-W`-quality machine evidence for a repo-local wrapper of pinned mathlib. It is not an
accepted `M0-W` state or release evidence. The frozen typed graph still truthfully records accepted
root closure as open because it predates these receipts; only the master may reconcile that state.

`AUDIT-Z` remains blocked. The dossier is `H1`, without an accepted pinpoint primary-source
edition/theorem/page/assumption/errata crosswalk and independent source review. It is `R4`, without
an independently reviewed complete structured reconstruction. Complete transitive provenance and
TCB acceptance are also absent.

`THEOREM-Z` additionally lacks an immutable clean snapshot, empty-cache network-denied cold build,
offline archive restoration, SBOM and license closure, two separately provisioned signed runner
attestations, an independently implemented minimal verifier, protected CI and required mutations,
and a deterministic content-addressed release bundle. Re-running the validator in this worker clone
cannot supply those gates.

## Commands and results

Commands were run in this worker clone at base revision
`60aae17521cd359d0473812b6927789cb4fee9e6` on 2026-07-12. No `lake update`, `lake build`, dependency
fetch/clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-0536` | 0 | Rank 593; lifecycle planned; theorem completion false. |
| `python3 Stage1_Instances/THM-M-0536/check_validation.py` | 0 | Exact root replay, trust profile, hashes, pins, and provenance passed; release gates stayed open. |
| `python3 Stage1_Instances/THM-M-0536/check_release.py` | 0 | Blocked decision, unaccepted dependency, provisional root evidence, false terminal booleans, and release cut set agree. |
| `python3 -m json.tool Stage1_Instances/THM-M-0536/release-decision.json` | 0 | Release decision is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0536 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The untracked `Formalizations/Lean/.lake` symlink was pre-existing, points to the canonical pinned
artifacts, and is excluded from changed paths and release evidence.

## Retry boundary

The integration lane must accept and reconcile the transitive phase receipts first. A separately
provisioned release lane must then close H0/R0 review, provenance and supply-chain evidence, cold
offline reproduction, independent attestations and verifier, mutation/CI gates, and deterministic
bundle validation. Only the master may accept the terminal decision.
