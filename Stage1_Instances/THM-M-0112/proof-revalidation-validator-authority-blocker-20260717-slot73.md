# THM-M-0112 proof revalidation blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0112-PROOF` at
worker base `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`). The sole task-state authority
already records the proof phase as `[_]` with one attempt. This revalidation
therefore proposes no second state transition and emits no second phase
receipt.

The exact claim tuple is `(v2_execution_rank=270, phase_layer=4,
phase_item_id=S56-M-0112-PROOF)`. The current theorem-DAG SHA-256 is
`95128825a99c9863fc09b6edc8a4a99ab5fae8e0927e40af88635f8945d2aa3e`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency Audit

The complete `parent_inspection_order`, direct-parent list,
transitive-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are empty. The empty sequence was traversed exactly once, in the supplied
order, before proof revalidation. No provider state, receipt, declaration,
reusable body, checkbox credit, or acceptance was consumed or inherited.

The integrated `dependency-reuse-ledger.json` has the required 1.1 schema and
truthfully records the same empty closure, but it is historical evidence bound
to graph `3d32f808...` and repository revision `2dc5a410...`. It was not
rewritten: the immutable validator pins those historical bytes, its mandatory
replay already fails, and a ledger-only rewrite could not create a lawful
current-base self-test. The adjacent JSON records the exact current empty
context without presenting the old ledger as fresh.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first worker-
unrepairable gate. The HEAD proof contract declares `check_proof.py` and
`check_proof.sh`; exactly one candidate exists and is unchanged at this worker
base:

```text
Stage1_Instances/THM-M-0112/check_proof.py
SHA-256 38adc855b256df295ae7e8769052541ef51a9e8e8b89e8afd21af29e74f47883
Git blob e0f659eab8dd3f3c30cecef6c1fa2c1f070d9c80
```

The exact contract-selected command was run:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0112/check_proof.py
```

It exited `1`, wrote zero stdout bytes, and wrote exactly
`validator base revision drifted\n` to stderr. Thus it emitted no
`stage1-validator-semantic-result/1.0` object. The validator hard-binds base
`2dc5a410...`, tree `841bdd61...`, graph `3d32f808...`, and proof cursor
`[ ]`/attempt zero, while the current claim is based at `c6ccce54...` with
cursor `[_]`/attempt one.

The validator is scheduler-owned and immutable in a worker handoff. This
worker did not create, refresh, replace, rename, or delete either candidate,
and did not wrap the legacy stderr prose in a manufactured semantic result.
The scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0112-PROOF.json` is also absent.

The sole `proof-receipt.json` remains the historical blocked receipt from
base `2dc5a410...`. It records `accepted=false`,
`phase_predicate_proven=false`, and `phase_accepted=false`. It was left
unchanged, and no second phase receipt was emitted. Because the current phase
is not genuinely self-tested, `.stage1-worker-selftest.json` is deliberately
absent.

## Kernel Boundary

An independent trust-zero replay against the pinned Lean environment confirms
the deeper mathematical encoding blocker. Fresh `/tmp` copies of
`Statement.lean` and `Proof.lean` elaborated successfully. The target-owned
declaration has exact type:

```text
Stage1Instances.THMM0112.Proof.not_weakTopologicalLefschetzTarget :
  Not (Stage1Instances.THMM0112.WeakTopologicalLefschetzTarget.{0, 0})
```

The countermodel takes `X=PUnit`, discrete `Y=Bool`, and complex dimension
two. All disconnected geometric proposition fields are true while `piMap` is
constant. The target then requires injectivity on degree-zero homotopy, but
the two path components of `Bool` have the same image. Lean reports only
`propext`, `Classical.choice`, and `Quot.sound` for this declaration.

This refutes the frozen abstract encoding, not the mathematical Lefschetz
hyperplane theorem. It gives no positive proof credit. The receipt's ten
positive obligations remain open, including the root cut
`M0112-B-BELOW` and `M0112-B-EDGE`; the obligation-tree predecessor is also
only `[_]`, not master-accepted `[x]`.

## Checks

Before adding this blocker, the Stage1 standard, theorem DAG, phase contract,
target manifest, statement, anchor audit, and obligation-tree checks passed.
The isolated trust-zero replay passed, and the scoped prohibited-construct
scan found no placeholder, bodyless declaration, unsafe injection, or oracle
escape. The automation-provided `.lake` symlink was reused read-only; no
`lake update`, `lake build`, dependency clone/fetch, or network operation ran.

After this pair was added, deterministic theorem-DAG generation expectedly
observed new target-owned evidence while the worker remains forbidden to
regenerate the read-only DAG projection. The post-artifact theorem-DAG and
aggregate standard checks therefore fail only at that scheduler integration
boundary.

## Retry Condition

The scheduler must publish a refreshed immutable `check_proof.py` and the
required per-item role map at an authoritative base that binds the current
graph, `[_]`/attempt-one cursor, ledger, sole receipt, and exact validation
recipe, then issue a fresh revalidation claim.

That mechanical repair cannot make the positive target provable. Positive
proof work also requires reopening `S56-M-0112-STATEMENT`, replacing the
disconnected geometric propositions and arbitrary `piMap` with faithful
native constructions and noncircular laws, accepting a new statement
fingerprint, and rerunning the dependent phases in exact DAG order.

This handoff is `no_state_change` with a blocked outcome. It claims no phase
receipt, worker self-test, state transition, provider acceptance transfer,
positive root proof, validation, release, audit completion, theorem
completion, or master acceptance.
