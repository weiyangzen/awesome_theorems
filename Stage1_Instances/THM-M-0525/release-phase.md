# THM-M-0525 release-phase decision

Item: `S56-M-0525-RELEASE`. Base revision:
`ff48a6d1083b7ce86e3b95f6417f4356ce5fc1a9`.

## Verdict

`blocked`; lifecycle remains `planned`; `audit_complete=false`; `theorem_complete=false`;
`release_accepted=false`. There are no accepted receipt IDs.

The exact frozen statement, conditional composition, local proof, and same-workspace independent
reconstruction have real Lean kernel evidence. That evidence does not satisfy the release gates.
The validation receipt is provisional and not master accepted; the frozen typed graph still records
the root open at `M2`; and the worker checkout reused a shared warm `.lake` cache. H0, R0, complete
transitive TCB/provenance, cold offline replay, SBOM/license closure, deterministic bundling, and
distinct-runner independent verification are also open.

The first failed dependency gate is
`dependency.S56-M-0525-VALIDATION.master_acceptance`. The first release-protocol failure is
`S56-10.6-HERMETIC-COLD-BUILD`. The exact machine decision and remaining root cut set are recorded
in `release-decision.json`.

## Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-0525/check_release.py` | 0 | Input hashes, frozen M2 root, all fail-closed release flags, and the blocked decision agreed. |
| `python3 Stage1_Instances/THM-M-0525/check_validation.py` | 0 | Exact local root and independent reconstruction replayed; the runner continued to report nonrelease boundaries. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets. |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0525` | 0 | Rank 582, lifecycle `planned`, theorem incomplete. |
| `python3 -m json.tool Stage1_Instances/THM-M-0525/release-decision.json >/dev/null` | 0 | Release decision is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0525 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

The existing pinned dependency artifacts were only read. No `lake update`, `lake build`, clone,
fetch, commit, push, checklist edit, or authoritative state edit was performed.

## Retry condition

The integration lane must first accept the prerequisite receipts and reconcile the structured root.
It must then close the foundation/TCB, provenance, H0, R0, hermetic cold/offline, supply-chain,
deterministic-bundle, and distinct-verifier gates on an immutable clean snapshot before deciding
`AUDIT-Z`, `THEOREM-Z`, or master acceptance.
