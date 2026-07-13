# THM-M-1237 validation-phase evidence

Item: `S56-M-1237-VALIDATION`. Base revision:
`c45f3c7090cb4adf616d45e5414985f956e807b2`; base tree:
`da6f991c07f11e8608ddc090af9356558d64d360`.

## Validation scope

The structured recipe re-elaborates the exact frozen statement and checked transport, the
conditional child-to-root composition, the proof phase's representative body and value-interface
counterexample, and a separately written countermodel in disposable output space. Every Lean
subprocess runs at trust level zero in a Bubblewrap network namespace with the host filesystem
read-only except for the temporary module directory.

`Validation.lean` imports `ObligationTree` but neither `Proof` nor its counterexample body. It uses a
one-valued input on a volume-null singleton with a zero whole-space extension; the proof phase used
zero input with a point spike. Both routes show that the frozen `ValueEstimateFamily` is false
because it quantifies over every almost-everywhere-equal representative and every constant,
including `C = 0`. This is a proof-architecture failure, not a counterexample to the canonical
existential `Statement`.

Kernel sorry checks pass, and checked proof/differential declarations report only `propext`,
`Classical.choice`, and `Quot.sound`. The validator binds the target-local hashes, frozen registry
denominator, proof receipt, tool identities, clean mathlib revision/tree/remote, two selected
mathlib source/blob/compiled-object hashes, and license. This is selected provenance and observed
trust only; it is not a complete transitive dependency graph, TCB closure, or SBOM.

## Commands and results

Commands ran from this worker clone on 2026-07-14 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No update, build, clone, fetch, checkout, dependency mutation,
or network operation ran.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets with ranks 1 through 1546 passed

python3 scripts/stage1_target.py show THM-M-1237
  exit 0: rank 175, planned L0/rework-required target; theorem_complete=false

bash Stage1_Instances/THM-M-1237/check_validation.sh
  exit 0 in 210 seconds: network-isolated trust-zero replay elaborated the exact statement,
  conditional composition, proof units, and separately written countermodel; five kernel sorry
  reports passed; stdout was 3411 bytes at SHA-256
  6619cc6585c4686fe5868a94581e2a2ff7ccf6a5f2a8844c6691ad4c9effd8ac

python3 -B Stage1_Instances/THM-M-1237/check_validation.py
  exit 0: exact replay, hygiene, selected trust/provenance, frozen hashes, pin, receipt, recipe,
  and worker packet passed; root, authority, hermetic, and independent gates failed closed

python3 -m json.tool Stage1_Instances/THM-M-1237/validation-spec.json
python3 -m json.tool Stage1_Instances/THM-M-1237/validation-receipt.json
python3 -m json.tool .stage1-worker-selftest.json
  exit 0 for each: valid JSON

git diff --check -- Stage1_Instances/THM-M-1237 .stage1-worker-selftest.json
  exit 0: no whitespace diagnostics, including no-index checks for untracked files
```

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Exact kernel replay | provisional pass | Exact statement/transport, conditional composition, representative body, and both interface countermodels elaborate under trust-zero network isolation. |
| Placeholder and unsafe boundary | pass | Kernel sorry reports and a comment-stripped scan found no placeholder, bodyless axiom/constant, opaque, unsafe/native/oracle, or external implementation construct. |
| Trust observation | provisional pass | Checked proof and differential declarations report only `propext`, `Classical.choice`, and `Quot.sound`; no theorem-specific foundation or complete TCB profile is accepted. |
| Selected provenance | provisional pass | Local hashes and selected pinned mathlib source/blob/olean identities, clean revision/tree/remote, manifest, license, and tool hashes agree; complete transitive provenance and SBOM remain open. |
| Exact root kernel closure | fail closed | `M1237-L-VALUE` is an invalid frozen interface and `M1237-L-HOLDER` remains unproved; the exact root stays `M3`. |
| Structured authority | fail closed | `S56-M-1237-PROOF` is only `[_]`; the frozen graph records no closed obligation and remains `root_closed=false`, with no closure master-accepted. |
| Hermetic replay | fail closed | Shared warm `.lake`; no separate immutable clean checkout, empty-cache bootstrap, offline restoration, complete TCB/SBOM, or deterministic release bundle. |
| Independent verification | fail closed | The differential countermodel shares this worker, checkout, kernel, and cache; no distinct verifier identity, clean provisioning, signature, or second attestation exists. |

The first node failure is `proof.M1237-L-VALUE.invalid_frozen_interface`; the first release failure
is `S56-10.6-HERMETIC-COLD-BUILD`. The vector remains `[H1, M3, R3]`.
`audit_complete=false` and `theorem_complete=false`; this evidence claims no `E0/E1`, accepted M0,
release, or master acceptance.
