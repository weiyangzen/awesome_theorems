# THM-M-0115 proof validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0115-PROOF` at
worker base `d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). It changes no theorem source,
prior receipt, task-state authority, theorem-DAG projection, lifecycle, debt
vector, item state, or scheduler-owned validator candidate.

The sole task-state authority records this item as `[_]` with one attempt and
its obligation-tree predecessor as `[_]` with one attempt. This run is a
current-base revalidation of unfinished worker evidence, not a new state
transition or master acceptance. The exact claim tuple is
`(v2_execution_rank=260, phase_layer=4,
phase_item_id=S56-M-0115-PROOF)`. The current theorem-DAG SHA-256 is
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`;
the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The authoritative `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all empty. The complete ordered closure was traversed exactly once,
before proof inspection, by inspecting zero providers. No provider phase
state, receipt, declaration body, reusable artifact, terminal proof body,
checkbox state, proof credit, or acceptance was consumed, copied, transported,
or inherited.

The tracked target-owned `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical proof evidence bound
to repository revision `307c34d30fc3763c82a944a142ae922b48ff18aa` and
theorem-DAG digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
not current-base evidence. A current ledger would bind the current graph,
context, base, and claim tuple while retaining the same empty collections.
It is deliberately not refreshed: the mandatory semantic replay below fails,
so no truthful current receipt or self-test handoff can consume a refreshed
ledger. This blocker records the current empty closure without presenting the
stale ledger as current evidence.

## First Failed Gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first worker gate
that cannot be repaired inside this assignment. The mandatory HEAD proof
contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and declares two scheduler-owned candidates:

- `Stage1_Instances/THM-M-0115/check_proof.py`
- `Stage1_Instances/THM-M-0115/check_proof.sh`

Exactly one exists at the worker base: `check_proof.py`, SHA-256
`f5d65c79d8cc4da1ae931b79ab77bab32280f14601b052f121f72617f493b792`,
Git blob `e7f38b0340a23a76fd1693f06c478911176bd1e8`. Its worktree bytes equal
the HEAD blob, so candidate selection is unambiguous. However, the immutable
candidate still requires obsolete base
`307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, theorem-DAG digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`,
and a worker packet tied to that base.

The exact contract-selected command was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py
```

It exited `1` and emitted exactly one
`stage1-validator-semantic-result/1.0` JSON object on stdout. The typed result
was `status=stale`, `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, `first_failed_gate=G09-FRESHNESS`, and
`stale_inputs=["HEAD"]`, with message `repository revision differs from worker
base`. This result proves neither the phase predicate nor phase acceptance.

The worker is forbidden to refresh, replace, rename, create, or delete a
validator candidate. Therefore this phase is not genuinely self-tested at the
current base. The historical `proof-receipt.json` remains bound to base
`307c34d3`; it is not refreshed or presented as current evidence, and no
`.stage1-worker-selftest.json` is emitted. The authority-owned per-item role
map `.cron/stage1-v2-app-server/role-maps/S56-M-0115-PROOF.json` is also absent
from this clone. That is a downstream master-lane blocker and does not
authorize a worker to manufacture the role map.

The phase contract requires exactly one `proof-receipt.json`. The tracked file
is that sole receipt, but it is stale and records the truthful blocked result.
This run therefore leaves it unchanged instead of emitting a second receipt
or rewriting historical evidence without an eligible semantic replay.

## Independent Kernel Blocker

Even after the scheduler-owned validator is refreshed, the assigned positive
proof predicate cannot close for the current frozen statement. An independent
trust-zero replay of the unchanged `Statement.lean` and `Proof.lean` succeeds.
The target-owned declaration

```text
Stage1Instances.THMM0115.Proof.not_grothendieckRiemannRochTarget :
  Not (Stage1Instances.THMM0115.GrothendieckRiemannRochTarget.{0, 0})
```

is placeholder-free and depends only on `propext`, `Classical.choice`, and
`Quot.sound`. It uses `Spec(Q)` with identity morphisms and `Int` for both
abstract theory carriers. Every semantic-label proposition is true, while the
unconstrained cap operations make the claimed equality reduce to `1 = 0`.

This refutes only the frozen abstract encoding, not mathematical
Grothendieck-Riemann-Roch. It closes zero positive obligations, supplies no
positive terminal body, and grants no M0 or acceptance credit. The frozen
registry still has 32 obligations, the root remains M3, and the machine cut
set remains `M0115-T-RELATIVE` and `M0115-T-TODD_ACTION`. The predecessor is
also authoritative `[_]`, not master-accepted `[x]`, so topology independently
blocks proof-phase acceptance.

## Checks Run

All checks ran from this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided `Formalizations/Lean/.lake` symlink was reused read-only;
no `lake update`, `lake build`, dependency clone/fetch, network command, or
cache mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups, the 1546-target set, v2 DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 blueprint states, typed relationships, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and 23 source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | All 1546 ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0115` | 0 | Rank 23; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| Declared candidate enumeration and HEAD/worktree blob comparison | 0 | Exactly `check_proof.py` exists and its blob is unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_proof.py` | 1 | One typed `repair_required` result reported obsolete validator base binding and `phase_accepted=false`. |
| Narrow `lake env lean --trust=0` replay of `Statement.lean`, then `Proof.lean` | 0 | The exact statement and negative countermodel elaborated; proof-output SHA-256 is `30974c6b4d80b58b371b8c0b2495c695bb0a35abc81818f75eb10b7572fe202b`; both declarations are sorry-free. |
| Scoped prohibited-construct scan over the target Lean sources | 1 | Expected no-match: no prohibited marker was found. |
| `git diff --check -- Stage1_Instances/THM-M-0115 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped handoff. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No false self-test handoff was emitted. |

The initial direct `lake env lean` attempt passed an external source path to
Lean while its project root was `Formalizations/Lean`; Lean rejected that path
containment before proof elaboration. The recorded successful replay instead
used the exact executable and `LEAN_PATH` returned by `lake env`, wrote only
temporary `/tmp/Statement.olean`, and then elaborated `Proof.lean`. The initial
invocation is a known command-shape failure, not kernel evidence.

Structural checks and the historical negative proof do not override the
scheduler-selected validator's typed failure. `audit_complete=false` and
`theorem_complete=false`.

## Retry Condition And Status Boundary

The scheduler/master lane must publish a refreshed `check_proof.py` whose
unchanged blob is already present at a fresh worker base and whose bindings
match that base, the current theorem DAG, dependency ledger, target artifacts,
and handoff protocol. The scheduler must also publish the authority-owned role
map. A fresh worker may then execute the exact selected argv and write exactly
one current receipt plus self-test handoff only if the typed result proves the
phase predicate.

That mechanical repair will not make the positive theorem provable. Reopen
`S56-M-0115-STATEMENT`; replace the disconnected semantic-label propositions
with faithful native constructions or noncircular law-bearing hypotheses that
constrain `KZero`, rational Chow homology, both pushforwards, both Chern
characters, tangent and Todd data, and cap actions. Accept a new statement
fingerprint, then freshly freeze and master-accept the anchor audit and
obligation tree before resuming positive proof work.

This artifact is a target-scoped blocker only. It grants no state transition,
proof-phase acceptance, accepted receipt ID, provider acceptance transfer,
root closure, validation, release, AUDIT-Z, THEOREM-Z, theorem completion, or
master acceptance.
