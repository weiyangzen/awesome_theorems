# THM-M-1084 validation-phase evidence

Item: `S56-M-1084-VALIDATION`. Base revision:
`2b8b16b4ca4c9ff610215bd8306fdb3f751f5345`; base tree:
`e9c3bddf01615e3a25aac732152cb0975f38f0eb`.

## Validation scope

The structured recipe re-elaborates the exact statement, the conditional final composition, the
implemented Gaussian-MGF and finite-cover declarations, and two separately written partial
reconstructions in disposable output space. Every Lean subprocess uses `--trust=0`, one Lean thread,
fixed locale and timezone, and a Bubblewrap network namespace. `Validation.lean` neither states nor
proves the Dudley root or either terminal package. Its differential checks corroborate only the
implemented partial bodies and are not distinct-runner evidence.

The exact target `Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget` remains open at `M3`.
`root_of_integrability_and_entropy_packages` consumes the unproved
`SupremumIntegrabilityPackage` and `EntropyInequalityPackage`; it is a valid conditional composition,
not a root proof. The frozen cut set remains `M1084-T-INTEGRABLE` and `M1084-T-ENTROPY`.

## Commands and results

Commands ran in this worker clone on 2026-07-15 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused without mutation. No `lake update`, `lake build`, dependency clone/fetch,
checkout, or network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1084
  exit 0: rank 526, planned L0/rework-required target; theorem_complete=false

python3 Stage1_Instances/THM-M-1084/check_statement.py
  exit 0: exact target expression and three structural mutations checked; expression SHA-256
  25bdfe85eaaa67694f865e6af60c240b013b2fbcd9acfb2949e5abdb0b34ca99

python3 Stage1_Instances/THM-M-1084/check_anchor_audit.py
  exit 0: six pinned Lean probes, immutable external near-candidate, and fail-closed status passed

python3 Stage1_Instances/THM-M-1084/check_obligation_tree.py
  exit 0: 16 obligations and 36 typed edges passed; root open at M3 with both terminal packages M4

bash Stage1_Instances/THM-M-1084/check_proof.sh
  exit 0: the exact Gaussian-MGF and finite-net bodies elaborated under --trust=0; seven audited
  declarations were sorry-free and used only propext, Classical.choice, and Quot.sound

python3 -B Stage1_Instances/THM-M-1084/check_validation.py
  exit 0: exact statement, conditional composition, seven partial proof bodies, and two
  same-worker differential partial reconstructions elaborated under network isolation; frozen
  hashes, hygiene, pin, and open-root decisions agreed

python3 -m json.tool Stage1_Instances/THM-M-1084/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1084/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

PYTHONPYCACHEPREFIX=/tmp/stage1-m1084-validation-pycache \
  python3 -m py_compile Stage1_Instances/THM-M-1084/check_validation.py
  exit 0: validator bytecode compiled outside the repository tree

rg -n --glob '*.lean' '<prohibited construct pattern>' Stage1_Instances/THM-M-1084
  exit 1 with empty output: expected pass; no placeholder, bodyless, unsafe, external,
  implementation escape, or native-oracle construct occurred in Lean source

git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics; untracked files also passed no-index checks
```

The snapshot-bound `check_proof.py` is intentionally not a validation recipe: it asserts the old
proof-phase base revision, pre-integration DAG state, and proof-phase dirty-file set. This phase binds
its committed proof receipt and inputs by hash, then replays the actual Lean declarations directly.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact statement replay | pass | The frozen target and checked expansion elaborate at the recorded expression fingerprint. |
| Conditional composition | pass, not root closure | The composition consumes both exact terminal packages; neither premise has a body. |
| Partial proof replay | pass | The Gaussian-MGF package is provisionally closed; finite-cover existence/attainment/positivity is genuine partial progress toward `M1084-C-NETS`. |
| Placeholder and unsafe boundary | pass | Lean sorry reports and a comment-stripped scan found no prohibited proof mechanism. |
| Trust observation | provisional pass | Checked declarations use only `propext`, `Classical.choice`, and `Quot.sound`; the instance foundation profile and complete TCB closure remain open. |
| Selected provenance | provisional pass | Frozen local hashes and clean pinned mathlib revision/tree/remote/license agree; complete transitive provenance and SBOM do not exist. |
| Structured authority | fail closed | `S56-M-1084-PROOF` is only `[_]`; no proof receipt or obligation is master-accepted. |
| Root kernel closure | fail closed | `M1084-T-INTEGRABLE` and `M1084-T-ENTROPY` have no proof bodies. |
| Hermetic replay | fail closed | Shared warm `.lake`; no clean checkout, empty-cache bootstrap, offline restoration, deterministic bundle, or complete TCB/SBOM. |
| Independent verification | fail closed | Differential partial checks share this worker, checkout, kernel, and cache; no distinct signed verifier or independent release checker exists. |

The first node gate is `dependency.S56-M-1084-PROOF.master_acceptance`; the first mathematical gate is
`proof.root_kernel_closure`; the first release gate is `S56-10.6-HERMETIC-COLD-BUILD`. The root
vector remains `[H1, M3, R3]`. `audit_complete=false` and `theorem_complete=false`. This packet
claims no E0/E1, M0, accepted state, complete validation, release, or master acceptance.
