# THM-M-0115 proof revalidation blocker

## Scope

This is the target-scoped fail-closed handoff for `S56-M-0115-PROOF` at
worker base `535924a30a83e9435b71f6163fe33bba6921212f` (tree
`0bce4f0de528486fc5f4e2b76a662697ca308883`). The authoritative proof cursor
is already `[_]` with one attempt, so this revalidation proposes no second
state transition and emits no second phase receipt.

The exact claim order is `(v2_execution_rank=260, phase_layer=4,
phase_item_id=S56-M-0115-PROOF)`. The supplied `parent_inspection_order` is
empty. That complete direct/transitive closure was traversed exactly once
before proof revalidation. There are no hard edges, reuse hints, or shared
groups, so no provider phase state, receipt, declaration body, reusable
artifact, checkbox state, proof credit, or acceptance was consumed or
transferred.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` fails before a lawful
current-base self-test can exist. The HEAD contract declares two
scheduler-owned candidates, and exactly one exists:

```text
Stage1_Instances/THM-M-0115/check_proof.py
```

Its SHA-256 is
`f5d65c79d8cc4da1ae931b79ab77bab32280f14601b052f121f72617f493b792`
and its unchanged HEAD Git blob is
`e7f38b0340a23a76fd1693f06c478911176bd1e8`. The exact contract-selected
command was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py
```

It exited `1` and emitted exactly one
`stage1-validator-semantic-result/1.0` object. The result was
`status=stale`, `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `first_failed_gate=G09-FRESHNESS`; the
stale input was `HEAD` because the validator freezes base `307c34d3...`,
whereas this claim runs at `535924a3...`. The scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0115-PROOF.json` is also absent.

The worker did not create, refresh, rename, replace, or delete either
validator candidate. The historical `proof-receipt.json` and
`dependency-reuse-ledger.json` remain bound to base `307c34d3...` and graph
`8be71ef1...`; they were not rewritten or presented as current evidence.
Refreshing only the ledger or receipt would violate the immutable validator's
pinned bytes and still would not prove the phase predicate. Therefore this
run deliberately leaves no `.stage1-worker-selftest.json`.

## Kernel boundary

Independent trust-zero replay confirms the deeper mathematical encoding
blocker. `Statement.lean` and `Proof.lean` both elaborated from scratch against
the existing pinned Lean artifacts. The proof output SHA-256 was
`30974c6b4d80b58b371b8c0b2495c695bb0a35abc81818f75eb10b7572fe202b`.
Both checked declarations were sorry-free and reported only `propext`,
`Classical.choice`, and `Quot.sound`.

The target-owned declaration

```text
Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget :
  Not (Stage1Instances.THMM0115.GrothendieckRiemannRochTarget.{0, 0})
```

uses `Spec(Q)` with identity morphisms and `Int` for both abstract theory
carriers. Every semantic-label proposition is true, while the unconstrained
cap operations make the claimed equality reduce to `1 = 0`. Thus the exact
frozen abstract target is false. This refutes only the current encoding, not
mathematical Grothendieck-Riemann-Roch, and grants zero positive proof credit.
All 32 positive obligations remain open; the machine cut set remains
`M0115-T-RELATIVE` and `M0115-T-TODD_ACTION`.

## Checks

Before adding this blocker pair, the Stage1 standard, theorem DAG, phase
contract, target manifest, and target display checks all passed. The narrow
trust-zero replay passed as described above. The automation-provided pinned
`.lake` symlink was used read-only; no `lake update`, `lake build`, dependency
clone/fetch, or network operation ran.

After this pair is added, deterministic theorem-DAG inventory checks are
expected to observe new target-owned evidence while this worker remains
forbidden to regenerate the read-only projection. Scheduler integration owns
that regeneration.

## Retry condition

The scheduler must first publish a refreshed immutable proof validator and
the required per-item role map at an authoritative base, then issue a fresh
claim containing those exact bytes. That mechanical repair will not make the
positive target provable. The statement must also be reopened and replaced
with concrete structures and laws binding `KZero`, rational Chow homology,
both pushforwards, both Chern characters, tangent and Todd data, and cap
actions. Statement, anchor-audit, and obligation-tree evidence must then be
refrozen and accepted in DAG order before proof work resumes.

This handoff is `no_state_change` with a blocked outcome. It claims no phase
receipt, self-test, state transition, root closure, M0, audit completion,
theorem completion, validation, release, or master acceptance.
