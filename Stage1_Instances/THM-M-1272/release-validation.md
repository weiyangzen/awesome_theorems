# THM-M-1272 release reconciliation

Item: `S56-M-1272-RELEASE`. Base revision:
`818d5a5c4333773091da1eab98b76f3ac87cfa12`; base tree:
`f833363d3cf0a9a67bd0b1ab128ec5e4796b16b1`.

## Exact verdict

The verdict is `blocked`. Lifecycle remains `planned`; the existing structured
root projection remains `[H2, M3, R4]` without acceptance and is disputed below;
and both `audit_complete` and `theorem_complete` are false. This worker accepts
no receipt and claims no `AUDIT-Z`, `THEOREM-Z`, release, or theorem completion.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`, specifically
`dependency.S56-M-1272-VALIDATION.master_acceptance`. The validation receipt is
only provisional worker evidence: `accepted=false` and `release_grade=false`.
Its recorded recipe is also stale after integration because it requires base
`e6c4d56e017f77b02752e6c1325f0298dfb7f4d4`, not this checkout's current base.

## Evidence reconciliation

The current narrow Lean check elaborates copied `Statement.lean`,
`ObligationTree.lean`, and `Proof.lean` at trust zero using the pinned toolchain.
It confirms four compactness obligations and reports only `propext`,
`Classical.choice`, and `Quot.sound`. The exact-root declaration still consumes
the explicit unproved `FountainMinimaxPackage`; it is conditional evidence, not
a root proof. The provisional mathematical cut is `M1272-N-SYMMETRIC`,
`M1272-C-MINIMAX`, `M1272-L-LINKING`, `M1272-C-DEFORMATION`, and
`M1272-T-LOWER-BOUND`.

No predecessor receipt is accepted, so accepted graph authority remains older
and weaker: it has no closed obligation IDs and still cuts
`M1272-T-LOWER-BOUND` plus `M1272-T-CRITICAL-LEVELS`. The target-local task DAG
still calls every phase open, the instance manifest still describes the
obligation-tree phase, and the old graph/specifications predate proof evidence.
This release phase records those inconsistencies without rewriting predecessor
state.

`AUDIT-Z` is independently blocked. The anchor audit's local
`audit_complete=true` means only that its bounded candidate-search phase was
self-tested; its receipt is unaccepted and it cannot override the overall
instance and validation booleans. The source crosswalk lacks an exact primary
theorem/page/edition/assumptions/errata mapping and independent H0 review.
Every required readable node remains R4 without independent R0 review.
The preserved H2 projection is itself unreconciled: the current ledger names
published candidates and open mappings, which supports H1 at best under
section 3.1, but it identifies no inspected primary-source condition or gap
needed for H2. This release worker records the conflict without rewriting
predecessor authority.

The first release-protocol failure is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. The automation-provided `.lake` symlink is
a shared warm pinned cache, not immutable clean release input, an empty-cache
cold build, or disconnected offline restoration. Complete foundation,
provenance, TCB, SBOM/license, independent-runner, minimal-verifier, protected
CI, and deterministic build-twice bundle evidence is absent.

## Commands and results

Commands ran from the repository root on 2026-07-14. No dependency update,
build, clone, fetch, checkout, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 targets and ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-1272` | 0 | Rank 165 remains planned, L0/rework-required, and theorem-incomplete. |
| `bash Stage1_Instances/THM-M-1272/check_proof.sh` | 0 | Current trust-zero warm-cache replay proved only the compactness package and conditional root. |
| `/usr/bin/bash Stage1_Instances/THM-M-1272/check_validation.sh` | 1 (expected) | The historical recipe failed closed at its stale repository-commit assertion before Lean replay. |
| `/usr/bin/bash Stage1_Instances/THM-M-1272/check_release.sh` | 0 | Network-denied cleared-environment replay reconciled hashes, structured authority, current narrow Lean evidence, stale validation, and every negative terminal gate. |
| `python3 -O -I -B Stage1_Instances/THM-M-1272/check_release.py` | 1 (expected) | The fail-closed guard rejected disabled assertions. |
| `python3 -m json.tool` on all release JSON files and `.stage1-worker-selftest.json` | 0 | All structured artifacts parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1272 .stage1-worker-selftest.json` | 0 | No whitespace errors. |

Retry can advance two independent workstreams: fully classify and reconcile the
inventory, source, and readable records for `AUDIT-Z`; and prove the minimax
package with exact fingerprints and graph/task reconciliation. A fresh,
dependency-legal validation receipt is then required. A separate release lane
must complete trust and supply-chain evidence, run cold/offline reproduction
and independent verification, and produce the deterministic bundle required
for `THEOREM-Z`.

Status boundary: this artifact self-tests only a negative release decision. It
supplies no accepted `M0`, `E0`, `E1`, `AUDIT-Z`, `THEOREM-Z`, release, theorem
completion, independent verification, or master acceptance.
