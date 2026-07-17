# THM-M-0115 validation blocker at HEAD d25efdf45

## Scope

This is the target-scoped fail-closed result for
`S56-M-0115-VALIDATION` at worker base
`d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). The exact claim tuple is
`(v2_execution_rank=260, phase_layer=5,
phase_item_id=S56-M-0115-VALIDATION)`.

The complete `parent_inspection_order` is empty. It was traversed exactly
once as the complete direct/transitive hard-parent closure. The target has no
hard edge, reuse hint, or shared group, so no provider phase state, receipt,
declaration body, reusable artifact, checkbox state, proof credit, or
acceptance was consumed or transferred. The current theorem-DAG SHA-256 is
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_missing` is the first
mechanically unrepairable worker gate. The immutable HEAD contract declares
these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0115/check_validation.py`
- `Stage1_Instances/THM-M-0115/check_validation.sh`

Neither exists in the worker base, current filesystem, or Git index. The
mandatory selection rule requires exactly one candidate already present at
the worker base with the same HEAD blob. The worker is forbidden to create,
refresh, rename, replace, or delete a candidate. There is consequently no
authority-selected argv and no possible stdout object with schema
`stage1-validator-semantic-result/1.0`. Exit-zero structural checks and prior
Lean evidence cannot substitute for the missing semantic replay.

The scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0115-VALIDATION.json` is also
absent, as is every contract candidate for the required validation
specification. This claim therefore deliberately emits no
`validation-spec.json`, no `validation-receipt.json`, and no
`.stage1-worker-selftest.json`.

The integrated `dependency-reuse-ledger.json` is a historical proof-phase
ledger bound to base `307c34d3...` and graph `8be71ef1...`. It truthfully
records the same empty closure, but it is stale for this validation claim.
Replacing it without a scheduler-selected replay or consumer receipt would
displace integrated proof evidence without satisfying validation, so the
companion JSON blocker records the fresh empty-closure audit instead.

## Positive validation boundary

Independent of the missing validator, topology and the positive validation
predicate fail closed:

- `S56-M-0115-PROOF` is authoritative `[_]`, not master-accepted `[x]`.
- `proof-receipt.json` has `accepted=false`, `verdict=blocked`, and closes
  none of the 32 positive obligations.
- Its sole scheduler-owned validator is itself stale at this HEAD; exact
  replay emitted one typed `G09-FRESHNESS` result with
  `phase_accepted=false`.
- Existing trust-zero evidence checks
  `Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget` with
  type `Not (GrothendieckRiemannRochTarget.{0,0})`, sorry-free and using only
  `propext`, `Classical.choice`, and `Quot.sound`.
- That countermodel refutes only the unconstrained abstract Lean encoding,
  not mathematical Grothendieck-Riemann-Roch, and grants no positive proof or
  validation credit.
- The frozen graph has `root_closed=false`, machine debt `M3`, no accepted
  closed obligations, and remaining machine cut set `M0115-T-RELATIVE` and
  `M0115-T-TODD_ACTION`.

Thus `audit_complete=false` and `theorem_complete=false`. No phase
acceptance, M0, AUDIT-Z, THEOREM-Z, accepted receipt, release grade, or
theorem-completion claim is supported.

## Bounded checks

Before adding this blocker pair, the Stage1 standard, theorem-DAG, phase
contract, ordered target manifest, and target display checks all passed. The
exact proof-validator command

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py
```

exited `1` and emitted exactly one
`stage1-validator-semantic-result/1.0` object with `status=stale`,
`verdict=repair_required`, `phase_accepted=false`, and
`first_failed_gate=G09-FRESHNESS`. Contract-derived validation-candidate
enumeration found zero present candidates.

The automation-provided pinned `.lake` symlink was only inspected. No
`lake update`, `lake build`, dependency clone/fetch, network access, or cache
mutation ran. After this pair is added, deterministic theorem-DAG inventory
checks may report the expected new-evidence drift; only integration may
regenerate that read-only authority.

## Retry condition

The scheduler/master lane must publish exactly one HEAD-tracked validation
validator and the per-item role map, then issue a fresh claim whose immutable
base contains those exact bytes. Positive validation also requires reopening
the unconstrained statement encoding, binding every formula operation to
source-faithful structures and laws, and accepting repaired statement,
anchor-audit, obligation-tree, and positive proof phases in exact DAG order.
The fresh claim must also contain the authority-bound validation specification
and a master-accepted proof receipt.

This blocker grants no worker state transition, validation acceptance,
provider acceptance transfer, proof credit, audit completion, theorem
completion, release, or master acceptance.
