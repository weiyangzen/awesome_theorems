# THM-M-0032 release decision

Item `S56-M-0032-RELEASE` has the exact verdict **blocked**. The lifecycle remains `planned`, the
current structured root vector remains `H1/M3/R4`, and both `AUDIT-Z` and `THEOREM-Z` are blocked.
`theorem_complete` and `audit_complete` remain false, with no accepted receipt IDs. This packet
self-tests a negative release reconciliation only; it is not theorem completion or release.

## Evidence reconciliation

The current narrow replay checks the exact frozen statement, the conditional Kaplansky composition,
and the real proof-phase regular-local domain package at Lean trust level zero. All four inspected
roots are sorry-free and report only `propext`, `Classical.choice`, and `Quot.sound`; the transitive
probe observes 22,572 declarations in 841 modules, with no unexpected bodyless or unsafe declaration.
This supports only provisional closure of `M0032-N-DOMAIN`.

The authoritative instance and typed graph accept no obligation or receipt and still record the
accepted machine cut as both `M0032-N-DOMAIN` and `M0032-A-PRIME-ELEMENT`. The newer proof and
validation receipts provisionally reduce the machine cut to `M0032-A-PRIME-ELEMENT`, but only the
master may reconcile that state. No placeholder-free inhabitant of `RegularLocalPrimeElementPackage`
exists in the pinned closure, so the exact UFD root is not kernel-closed.

The first failed workflow gate is `S56-10.2-DEPENDENCY-ACCEPTANCE`: validation is `[_]`, its receipt
is explicitly unaccepted and non-release-grade, and it transitively depends on an unaccepted proof
receipt. `AUDIT-Z` independently fails because the authoritative graph and public dossier predate the
domain proof and the frozen anchor inventory predates the later discovery of the exact but incompatible
mathlib PR #39510 candidate. That draft candidate uses Lean 4.32.0-rc1 and seven modules absent from
the pin; it was neither imported nor credited. H0/R0 and complete trust, provenance, and workflow
records also remain open.

The first release-specific failure is immutable clean input, followed by
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE-REPLAY`. The replay uses the existing canonical pinned shared
`.lake` artifacts. There is no empty-cache cold build, offline archive restoration, complete SBOM and
license closure, deterministic signed bundle, two independently provisioned attestations,
independently implemented minimal verifier, or protected adversarial CI evidence.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (`Asia/Shanghai`). No `lake update`, `lake build`,
dependency clone/fetch/checkout, or `.lake` mutation was performed.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | rank 1076; planned; L0/rework-required; theorem incomplete |
| `bash Stage1_Instances/THM-M-0032/check_proof.sh` | 0 | fresh temporary Statement, ObligationTree, and DomainProof files elaborated at trust zero; the domain package is sorry-free with exactly the three observed axioms |
| separate temporary `lake env lean --trust=0 -t0` replay of Statement, AnchorAudit, ObligationTree, DomainProof, and Validation under bubblewrap | 0 | exact output hashes matched the validation receipt; four roots, 22,572 declarations, 841 modules, three observed axioms, no unexpected bodyless or unsafe declaration |
| `python3 -I -B Stage1_Instances/THM-M-0032/check_release.py` | 0 | current authority and target hashes, the prior replay receipt and tool identity, dependency staleness, negative decision, receipt, and worker packet agree |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0032/check_validation.py --probe` | 1 | expected stale-receipt probe: the historical checker is bound to base `289e3709...`, not this release snapshot |
| execute `release-spec.json` `argv` without shell interpolation | 0 | authority, target hashes, dependency staleness, narrow replay, negative decision, receipt, and worker packet agree |
| `python3 -m json.tool .stage1-worker-selftest.json` and one invocation for each of `release-spec.json`, `release-decision.json`, and `release-receipt.json` | 0 | all four structured artifacts parsed |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0032-release-pycache python3 -m py_compile Stage1_Instances/THM-M-0032/check_release.py` | 0 | checker syntax passed without generated files under the owned path |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` | 0 | no whitespace diagnostics |

Retry requires dependency-ordered master review and authoritative graph/inventory reconciliation,
then a compatible exact terminal integration or a proof of `M0032-A-PRIME-ELEMENT`, independent
H0/R0 acceptance, complete trust and provenance closure, cold offline reproduction, supply-chain
closure, independent verification, and a deterministic bundle accepted by the master lane.
