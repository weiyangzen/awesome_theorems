# THM-M-0927 validation-phase evidence

Item: `S56-M-0927-VALIDATION`. Base revision:
`c93e664d3a7e0383b037cfa2d5e47ba14adfb2cb`; base tree:
`d8ea21a05ed52ff43d984128352a07f479aae6e6`.

Validation ran on 2026-07-15 (Asia/Shanghai) against the exact frozen
natural-index real-valued radical formula. The worker added no proof content
to the proof-phase declaration.

## Verdict

`blocked_after_self_test_pending_master_acceptance`. Fresh trust-level-zero
outputs for `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and a
differential `Validation.lean` replay all elaborate. The proof root and the
fresh direct recomposition have the exact type `BinetFormulaTarget`. The four
checked declarations are sorry-free and use exactly `propext`,
`Classical.choice`, and `Quot.sound`. Lean reports a 12,891-declaration,
509-module root closure with no unexpected bodyless or unsafe declaration.

Selected provenance checks bind pinned mathlib revision, tree, remote, license,
the `GoldenRatio.lean` Git blob, complete source hash, lines 180-195 body hash,
compiled artifact hash, and a clean package worktree. The exact proof remains
provisional: `S56-M-0927-PROOF` is only `[_]`, while the accepted instance and
typed graph still record `[H1, M3, R4]`, zero accepted obligations, and no
accepted receipts.

This is nonrelease evidence. Bubblewrap denies network and makes the host root
read-only, and target outputs are fresh, but dependencies come from the shared
warm automation `.lake`. There is no clean empty-cache cold bootstrap,
offline-restorable archive, complete transitive TCB/provenance/SBOM packet,
deterministic release bundle, or distinct signed runner. The differential root
does not call the proof root, but shares its worker, checkout, toolchain,
mathlib body, and cache, so it is not independent verification.

## Commands and results

No `lake update`, `lake build`, dependency clone/fetch, network fetch, or
`.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at ranks 1 through 1546 passed. |
| `python3 scripts/stage1_target.py show THM-M-0927` | 0 | Rank 1546; planned, L0/rework-required, theorem incomplete. |
| structured Bubblewrap argv in `validation-spec.json` with `--probe` | 0 | Network-isolated fresh trust-zero replay, root closure inspection, selected provenance, and fail-closed decisions passed before final receipt creation. |
| structured Bubblewrap argv in `validation-spec.json` | 0 | Final receipt, worker packet, exact kernel/trust/provenance observations, and fail-closed decisions passed. |
| independent agent: fresh temporary trust-zero `Statement -> ObligationTree -> Proof` replay | 0 | Exact proof declarations elaborated; three sorry-free reports and exact observed axiom set passed. |
| independent agent: separately written direct root plus current `Validation.lean` replay | 0 | Exact root elaborated; closure was 12,891 declarations across 509 modules, with no unexpected bodyless or unsafe declaration. Same runner/cache, therefore not the rev-5.6 independent-runner gate. |
| `python3 -m json.tool` on `validation-spec.json`, `validation-receipt.json`, and `.stage1-worker-selftest.json` | 0 | All structured artifacts parsed. |
| `PYTHONPYCACHEPREFIX=/tmp/stage1-m0927-validation-pycache python3 -m py_compile Stage1_Instances/THM-M-0927/check_validation.py` | 0 | Validator compiled outside the repository. |
| `PYTHONOPTIMIZE=1 python3 -B Stage1_Instances/THM-M-0927/check_validation.py --probe` | 1 expected | Fail-closed guard rejected disabled assertions. |
| `git diff --check -- Stage1_Instances/THM-M-0927 .stage1-worker-selftest.json` | 0 | No scoped whitespace diagnostics. |

The inherited proof checker is not cited as current replay evidence because it
intentionally binds the earlier proof worker revision and packet. This phase's
validator independently binds the integrated proof inputs and current base,
then performs the fresh Lean replay directly.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | The frozen statement, conditional tree, exact proof root, and differential direct recomposition elaborate from fresh target outputs at trust zero. |
| Placeholder/unsafe boundary | provisional pass | Parser-aware source scans, `assert_no_sorry`, `#print sorries`, and root-closure inspection find no prohibited device or unexpected bodyless/unsafe declaration. |
| Selected provenance | provisional pass | Immutable mathlib identities, terminal source/body/olean, Apache-2.0 license, tool inputs, and clean pinned package agree. |
| Dependency authority | fail closed | Proof is not master accepted; accepted receipts and obligation closure remain empty. |
| Complete trust/provenance | fail closed | No accepted foundation profile or complete transitive declaration/source/compiled-artifact TCB and SBOM inventory exists. |
| Source/readability | fail closed | Primary-source H0 and independently reviewed R0 remain absent. |
| Hermetic release | fail closed | Shared warm `.lake`; no clean checkout, empty-cache cold bootstrap, offline restoration, or deterministic bundle. |
| Independent verification | fail closed | No distinct signed identity, independently provisioned checkout/cache, second attestation, or independent minimal verifier. |

The first node failure is
`dependency.S56-M-0927-PROOF.master_acceptance`. The first release failure is
`S56-10.6-HERMETIC-COLD-EMPTY-CACHE`. This self-tested validation
implementation proposes only worker state `[_]`. It grants no accepted M0-W,
E0/E1, H0, R0, AUDIT-Z, THEOREM-Z, release, theorem completion, or master
acceptance.
