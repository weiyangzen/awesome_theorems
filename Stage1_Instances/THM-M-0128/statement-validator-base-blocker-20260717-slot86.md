# THM-M-0128 statement validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0128-STATEMENT` at
worker base `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`). It changes no theorem source,
phase receipt, dependency ledger, validator, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

The authoritative claim key is
`(v2_execution_rank=280, phase_layer=1, phase_item_id=S56-M-0128-STATEMENT)`.
The current theorem-DAG SHA-256 is
`95128825a99c9863fc09b6edc8a4a99ab5fae8e0927e40af88635f8945d2aa3e`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Authoritative current state

The sole task-state authority, `Docs/Stage1_Blueprint_v2.md`, records both
`S56-M-0128-INTAKE` and this statement item as `[_]` with one attempt. Under
the dual-cursor protocol, `[_]` is unfinished worker-self-tested evidence, not
master acceptance. This worker neither redoes nor promotes it. The theorem-DAG
projection agrees and records no direct hard parent, transitive hard ancestor,
hard edge, reuse hint, or shared lemma group.

The tracked statement receipt is truthful historical negative evidence, not a
positive statement result. It has schema `stage1-node-receipt/1.0`, SHA-256
`1152f14553cbd100450e3787a35e6946f9f5076f8317b1a0139c40a6a3c453d5`,
Git blob `bd30606eb78eab8c2b66af0564b4aa471d2a1294`, `accepted=false`,
`verdict=blocked`, no statement fingerprint, and four undefined mutations. It
binds base `dae1951609072752d49d111bf00e78e4512f2d14`, tree
`9d8cc27cc0e09489c78b0bdbdeb57b15c5840f13`, and obsolete theorem-DAG
digest `3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa`.
Provider or predecessor acceptance is not inherited.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_stale` is the first mechanically
unrepairable worker gate. The mandatory HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and Git blob `84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For the statement phase it
declares exactly these scheduler-owned candidate paths:

- `Stage1_Instances/THM-M-0128/check_statement.py`
- `Stage1_Instances/THM-M-0128/check_statement_artifacts.py`

Exactly one exists at this worker base: `check_statement.py`, SHA-256
`212251f3154a8b8ca6747e983655e279ca754e875de6e23cdca50aa644db42b1`,
Git blob `25b60d1e6f3216c53e5015d53eea953d9bcc0c79`. Its worktree bytes equal
HEAD and worker-base bytes; the worker did not modify it. The exact
authority-selected replay was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py
exit: 1
stdout: {"audit_complete":false,"blocked":false,"first_failed_gate":"S01-ARTIFACTS.negative_evidence_validation","item_id":"S56-M-0128-STATEMENT","message":"theorem DAG changed","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0128","verdict":"repair_required"}
```

The validator is immutable in this worker lane and hard-codes the earlier
base, tree, graph digest, statement packet, and empty ledger. In fact it did
not exist at its embedded base, so its blob cannot satisfy the contract's
candidate-at-worker-base rule for that historical packet. At the current base
it rejects the authoritative theorem-DAG bytes before reaching the negative
statement predicate. Its stdout is exactly one typed semantic object, but its
semantics are `status=failed`, `verdict=repair_required`,
`phase_accepted=false`, and `phase_predicate_proven=false`; exit code or other
successful checks cannot override that result.

The worker is forbidden to refresh, replace, rename, create, or delete any
declared validator candidate. Consequently this run writes no replacement
phase receipt and no root `.stage1-worker-selftest.json`. Refreshing the
receipt or handoff without a lawful scheduler-selected replay would
manufacture evidence.

## Dependency and reuse audit

The supplied `parent_inspection_order` is exactly `[]`. The direct-hard-parent,
transitive-hard-ancestor, hard-edge, reuse-hint, and shared-group lists are also
exactly empty. The complete required closure was traversed exactly once as the
empty sequence before any proof work. No parent state, receipt, declaration
body, reusable artifact, terminal proof body, import, copy, transport,
checkbox state, proof credit, or acceptance was consumed or inherited. No
proof work was performed. The empty declared context is not a claim of
mathematical independence.

The tracked `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully contains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical anchor-audit packet
evidence bound to repository revision
`74d4c272070069bc62df15798895293b4795940a`, graph digest
`cb4b83c4c4a5474fce51f98098f1421315fe7f1bd8cd52205932e57eced9f675`,
and the anchor-audit claim key. It is not rewritten here: a ledger-only change
cannot repair the scheduler-owned semantic validator and would further stale
the tracked statement receipt.

## Positive statement gate remains open

Independently of validator freshness, `S02-EXACT-TARGET` and `S03-MUTATIONS`
remain open. Repository evidence identifies the CM-special-point family of
Shimura reciprocity, the 1971 Shimura monograph, and the 1961
Shimura-Taniyama source family, but it does not select an immutable exact
theorem/page or reconcile incorporated definitions, hypotheses, translations,
corrections, and errata. The CM field versus CM algebra, CM type, reflex norm,
idele versus idele class, arithmetic versus geometric Artin map, canonical
model and level, action variance, and equality versus orbit conventions all
remain root-relevant and unresolved. Choosing convenient conventions would
broaden, narrow, or reverse the requested theorem.

The pinned environment exposes only the adjacent `NumberField.IsCMField` and
`NumberField.AdeleRing` substrate used here. The unchanged `Statement.lean`
has exactly the two corresponding direct imports and deliberately declares no
canonical proposition. Its trust-zero elaboration succeeds, but that proves
only the availability of those substrate types. There is still no exact
expression, statement or environment fingerprint, credited transport,
canonical-target import-minimality result, or meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutation. The intake
predecessor is also only `[_]`, not master-accepted `[x]`, which independently
prevents dependency-ordered master closure.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, checkout,
network action, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Fifteen assurance groups, all 1546 uniform-L0 targets, the v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | All 1546 theorem nodes, 10822 phase states, typed relations, state preservation, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0128` | 0 | Rank 46, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Declared candidate enumeration and HEAD/base/worktree blob comparison | 0 | Exactly one statement candidate exists, and its bytes are unchanged. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0128/check_statement.py` | 1 | One typed `failed` / `repair_required` object reported the stale embedded theorem-DAG binding; `phase_accepted=false`. |
| `cd Formalizations/Lean && LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC timeout --foreground --kill-after=5s 300s lake env lean --trust=0 ../../Stage1_Instances/THM-M-0128/Statement.lean` | 0 | The unchanged CM-field and adele-ring boundary probe elaborated; no exact-target credit is claimed. |
| Prohibited-token scan of `Statement.lean` | 1, expected no matches | No `sorry`, axiom, placeholder, unsafe, or native-oracle construct was present. |
| `git diff --check -- Stage1_Instances/THM-M-0128 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped delta. |

The structural and Lean checks are bounded supporting observations. They do
not replace the failed scheduler-selected semantic replay or prove the
positive statement predicate.

## Retry condition and status boundary

The scheduler/master lane must publish a current-base-compatible
`check_statement.py`, or exactly one other declared candidate, in an
authoritative commit and issue a fresh claim whose worker base contains the
identical validator blob. A fresh worker can then refresh the statement-owned
empty dependency ledger and exactly one phase receipt and replay the selected
argv. Positive phase acceptance independently requires intake master
acceptance, an independently approved immutable source theorem/page, complete
convention and boundary mapping, a pinned concrete CM/reflex/Shimura object
model, an exact kernel-elaborated expression and environment fingerprint,
checked transports, minimal canonical imports, and all four mutation classes.

This blocker grants no state transition, phase acceptance, accepted receipt,
exact-statement credit, proof credit, provider acceptance transfer, audit
completion, theorem completion, or master acceptance.

## Persisted-goal continuation audit

The next automatic continuation re-read the same worker base and tree, the
same `[_]` cursor with one attempt, the same graph/context digests, the same
empty parent closure, and the same unique unchanged validator blob. The exact
contract-selected replay again exited `1` and emitted the same single typed
`failed` / `repair_required` object with message `theorem DAG changed` and
`phase_accepted=false`. No scheduler-owned validator repair or new base has
appeared, so a lawful current-base receipt and self-test handoff remain
impossible; `.stage1-worker-selftest.json` is still intentionally absent.

The third consecutive persisted-goal audit again observed that identical
base/tree, `[_]` cursor, graph/context, empty dependency closure, and unique
validator blob. The mandatory replay again exited `1` with the identical
typed `S01-ARTIFACTS.negative_evidence_validation` result and message
`theorem DAG changed`. The blocking condition has therefore repeated across
the original worker turn and two automatic continuations. The worker is at an
external scheduler-ownership impasse: only an authoritative validator/base
repair can permit a truthful receipt and self-test packet.
