# THM-M-0115 proof revalidation blocker

## Scope

This is the target-scoped fail-closed handoff for `S56-M-0115-PROOF` at
worker base `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`). The sole task-state authority
already records proof as `[_]` with one attempt, so this run proposes no
second transition and emits no second phase receipt.

The exact claim order is `(v2_execution_rank=260, phase_layer=4,
phase_item_id=S56-M-0115-PROOF)`. The supplied `parent_inspection_order` is
empty. That complete direct and transitive closure was traversed exactly once
before proof revalidation. There are no hard parents, ancestors, reuse hints,
or shared groups, so no provider state, receipt, body, reusable artifact,
proof credit, or acceptance was consumed or transferred.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` prevents a lawful
current-base self-test. The HEAD contract declares two scheduler-owned
candidates, and exactly one exists:

```text
Stage1_Instances/THM-M-0115/check_proof.py
```

Its SHA-256 is
`f5d65c79d8cc4da1ae931b79ab77bab32280f14601b052f121f72617f493b792`
and its unchanged HEAD Git blob is
`e7f38b0340a23a76fd1693f06c478911176bd1e8`. The exact selected command was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py
```

It exited `1` and emitted exactly one
`stage1-validator-semantic-result/1.0` object. The semantic result was
`status=stale`, `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, and `first_failed_gate=G09-FRESHNESS`; its
only stale input was `HEAD`. The validator freezes base `307c34d3...` and
graph `8be71ef1...`, while this claim runs at `c6ccce54...` with graph
`95128825...`. The required scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0115-PROOF.json` is also absent.

The worker did not create, refresh, rename, replace, or delete a validator
candidate. The historical `proof-receipt.json` and
`dependency-reuse-ledger.json` remain bound to base `307c34d3...`; neither
was rewritten or presented as current evidence. Refreshing them alone cannot
pass the immutable validator because it rejects current `HEAD` before reading
them and also pins their historical bytes. Therefore this run deliberately
leaves no `.stage1-worker-selftest.json`.

## Kernel boundary

An independent `--trust=0` replay against the existing pinned artifacts still
elaborates both `Statement.lean` and `Proof.lean`. Statement output SHA-256 is
`bfff4eb71b922d3feaf598391d55b7e404d8fe5ebbd7c8a5691ce128288a52cf`;
proof output SHA-256 is
`30974c6b4d80b58b371b8c0b2495c695bb0a35abc81818f75eb10b7572fe202b`.
Both checked negative declarations are sorry-free and report only `propext`,
`Classical.choice`, and `Quot.sound`.

The target-owned theorem

```text
Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget :
  Not (Stage1Instances.THMM0115.GrothendieckRiemannRochTarget.{0, 0})
```

uses `Spec(Q)` with identity morphisms and `Int` carriers. Every semantic-label
proposition is true while the unconstrained cap actions reduce the target
formula to `1 = 0`. This refutes only the current abstract Lean encoding, not
mathematical Grothendieck-Riemann-Roch, and gives no positive proof credit.
All 32 positive obligations remain open; the machine cut set remains
`M0115-T-RELATIVE` and `M0115-T-TODD_ACTION`.

## Checks

Before adding this blocker pair, the phase-contract, Stage1 standard, theorem
DAG, target manifest, and target display checks all passed. The narrow Lean
replay passed as described above. The automation-provided pinned `.lake`
symlink was used read-only; no `lake update`, `lake build`, dependency fetch,
clone, or network operation ran.

After this pair is added, deterministic theorem-DAG inventory checks are
expected to observe new target-owned evidence while this worker remains
forbidden to regenerate the read-only projection. Scheduler integration owns
that regeneration.

## Retry condition

The scheduler must publish a refreshed immutable proof validator and the
required per-item role map at an authoritative base, then issue a fresh claim
containing those exact bytes. That mechanical repair cannot make the positive
target provable. The statement must also be reopened and replaced with
concrete structures and laws binding `KZero`, rational Chow homology, both
pushforwards, both Chern characters, tangent and Todd data, and cap actions.
Statement, anchor-audit, and obligation-tree evidence must then be refrozen and
accepted in DAG order before positive proof work resumes.

This handoff is `no_state_change` with a blocked outcome. It claims no phase
receipt, self-test, state transition, root closure, M0, audit completion,
theorem completion, validation, release, or master acceptance.
