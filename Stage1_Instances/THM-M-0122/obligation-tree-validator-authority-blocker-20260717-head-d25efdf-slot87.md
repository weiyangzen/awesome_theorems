# THM-M-0122 obligation-tree validator authority blocker

## Result

`S56-M-0122-OBLIGATION_TREE` cannot produce a truthful current phase receipt or
worker self-test handoff at base
`d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). The sole task-state authority
records the item as `[_]` with one attempt, and the exact claim tuple is
`(275, 3, S56-M-0122-OBLIGATION_TREE)`.

The HEAD phase contract selects exactly one scheduler-owned candidate:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0122/check_obligation_tree.py
```

The file is unchanged from HEAD (SHA-256
`7ad5b4a29d947ed40f6d740a8aefb9fef3347ea24d4a3dac448af55b62e90f4c`,
Git blob `0e4dce455d894d03c300c65a11b531b3b652c8c5`), and the alternate
candidate is absent. Its embedded base and dependency bindings are obsolete.
The exact replay exited `1`, wrote empty stderr, and emitted exactly one typed
semantic result:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"OBLIGATION-TREE-SEMANTIC-CHECK","item_id":"S56-M-0122-OBLIGATION_TREE","message":"repository base revision drift","open_obligations":23,"phase":"obligation_tree","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0122","verdict":"repair_required"}
```

Exit zero is not inferred, and the typed negative verdict cannot support
master acceptance. Worker rules forbid refreshing, replacing, renaming, or
deleting the candidate. Therefore this run creates no
`stage1-node-receipt/1.0` and leaves `.stage1-worker-selftest.json` absent.

## Dependency and reuse audit

The supplied `parent_inspection_order` is exactly `[]`. It was traversed
exactly once before proof work and is the complete direct and transitive
hard-parent closure. The direct-parent, transitive-ancestor, hard-edge, and
reuse-hint sets are empty. No parent state, receipt, declaration, terminal
body, reusable artifact, checkbox, or acceptance was consumed.

The current graph has one nonblocking shared group,
`SHARED-MODULE-dff4d00d3b45e946`. Its identity is
`Atlas.ArithmeticGeometry.code.FaltingsTheorem`, with members `THM-M-0122`
and `THM-M-0123`. Current HEAD inspection of `THM-M-0123` found only
provisional intake, statement, and anchor-audit evidence and no obligation
tree or proof body. Its anchor audit binds the Atlas file at SHA-256
`b5aca9ae03c178c908fdf0e28d4dd8672643b16390b25e9b9771882726ed8f01`
and records `faltings_theorem` as directly `by sorry` and materially
mismatched. Its anchor receipt is `accepted=false`.

The group decision is `not_applicable`: no exact import, copy, wrapper,
checked transport, validation receipt, provider checkbox, or evidence credit
is used. The current schema-1.1 audit is recorded in
`dependency-reuse-ledger-obligation-tree-head-d25efdf-slot87.json`. The
integrated canonical ledger remains historical proof-phase evidence and is not
overwritten with a packet the mandatory validator cannot validate.

## Preserved architecture

The integrated obligation registry still freezes 23 canonical obligations at
denominator
`fa58b3f6f5f390a8fd776a0d789158582ec5ded0f22616a94460d6eb0306a508`.
The typed bundle contains seven graph families and 56 edges, and
`ObligationTree.lean` has SHA-256
`c081ee9e08e5bf5aeb3060605ebc9c7f7926d08d04632380e105e8ff1c783c69`.
Those bytes are unchanged. They remain a substantial architecture candidate,
but the failed mandatory replay prevents a current self-test claim. The later
provisional proof receipt does not imply this phase is accepted.

The mathematical root remains open at finite-extension normalization,
Jacobian and Abel-Jacobi construction, Mordell-Weil, Mordell-Lang,
no-positive-coset, and finite-intersection bodies. `audit_complete=false` and
`theorem_complete=false`.

## Retry

The scheduler/master lane must publish a current-bound, HEAD-tracked
`check_obligation_tree.py` and issue a fresh claim containing that unchanged
blob. It must bind the fresh base, graph SHA-256
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`,
context SHA-256
`0c0f6d1bed857aeaad7b4656db6ae6fe5c9c6bde39f7c9fb9ec2f8938eb4a484`,
the `[_]` attempt-one state, and the weak-group non-reuse decision. A fresh
worker can then refresh the canonical ledger and exactly one receipt, replay
the unchanged validator, and write the required handoff.

This blocker grants no phase closure, state transition, proof credit,
provider acceptance, `AUDIT-Z`, `THEOREM-Z`, theorem completion, release, or
master acceptance.

## Bounded checks

No network, `lake update`, `lake build`, dependency clone/fetch, or `.lake`
mutation was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0122` | 0 | Rank 41, planned lifecycle, legacy evidence unaccepted, theorem incomplete. |
| exact contract-selected validator argv | 1 | Typed `repair_required`; `phase_accepted=false`; base revision drift. |
| JSON syntax checks for the two structured artifacts | 0 | Both files parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-0122` | 0 | No whitespace errors. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Expected integration boundary: target-owned blocker evidence changes deterministic evidence inventory, while the worker may not regenerate the authority-owned DAG. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Delegates to the same expected authority-owned DAG integration boundary. |
