# THM-M-0403 validation-phase result

Item `S56-M-0403-VALIDATION` was executed against the proof-phase snapshot.
The node-scoped kernel, placeholder, pin, and proof-provenance checks pass for
the partial declarations in `Proof.lean`. This does not close the canonical
root: the proof receipt itself has no closed obligation, the frozen graph has
no composition certificate, and `M0403-L-ESS-FINITE` remains the minimal open
root cut.

## Exact result

The structured recipe in `validation-spec.json` was run from repository root:

```text
python3 Stage1_Instances/THM-M-0403/validate_phase.py
  exit 0
  ok: pinned Statement.lean and Proof.lean elaborated in a fresh temporary module directory
  ok: six proof declarations report only propext, Classical.choice, and Quot.sound
  ok: proof provenance hashes and pinned clean mathlib revision match the proof receipt
  open: root M4; no closed obligations or composition certificate; cut set M0403-L-ESS-FINITE
  blocked: cold hermetic replay, complete TCB/SBOM, and distinct-runner independent verification
```

The validator invokes `lake env lean` narrowly, writes temporary `Statement.olean`
output outside the dependency tree, and removes it. It verifies the exact pinned
mathlib commit and requires its checkout to be clean. No update, build, clone,
fetch, or dependency mutation is performed.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The statement and six partial/conditional proof declarations elaborate against pinned Lean/mathlib. |
| Placeholder and unsafe scan | pass | No `sorry`, `admit`, local `axiom`, or `unsafe` declaration occurs in `Statement.lean` or `Proof.lean`. |
| Axiom profile observation | provisional pass | All six printed declarations use only `propext`, `Classical.choice`, and `Quot.sound`; no accepted release-grade profile or full TCB receipt exists. |
| Proof provenance | pass for partial bodies | Source and registry/graph hashes match `proof-receipt.json`; mathlib is at the pinned clean revision. |
| Exact root kernel closure | fail | The only root composition theorem takes the desired finite-zero-set result as an explicit premise. No root theorem or closed frozen obligation exists. |
| Hermetic release replay | fail closed | The worker reuses a shared writable canonical `.lake` symlink and warm compiled artifacts. There was no new clean checkout, empty-cache cold build, offline archive replay, SBOM/license closure, or complete executable/olean TCB inventory. |
| Independent verification | fail closed | This is one worker in one mutable clone. There is no second identity, independently provisioned clean runner, second signed attestation, or independently implemented minimal verifier. |

This validation node is self-tested as a truthful negative theorem-validation
result. It supplies no `E0/E1`, `M0-*`, `AUDIT-Z`, `THEOREM-Z`, release, or
master-acceptance credit. The root remains `[H1, M4, R3]`, with
`audit_complete=false` and `theorem_complete=false`.
