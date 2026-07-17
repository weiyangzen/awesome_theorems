# THM-M-0129 statement validator-base blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0129-STATEMENT` at
worker base `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`). It changes no Lean source,
phase receipt, dependency ledger, validator candidate, task-state authority,
theorem-DAG projection, lifecycle, debt vector, or acceptance state.

The exact claim tuple is
`(v2_execution_rank=281, phase_layer=1, phase_item_id=S56-M-0129-STATEMENT)`.
The assigned and observed theorem-DAG SHA-256 is
`95128825a99c9863fc09b6edc8a4a99ab5fae8e0927e40af88635f8945d2aa3e`;
the stable target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Authoritative state

The sole task-state authority, `Docs/Stage1_Blueprint_v2.md`, records both
`S56-M-0129-INTAKE` and this statement item as `[_]`, with one attempt each.
Under the rev-5.6 dual-cursor protocol, `[_]` is unfinished worker-self-tested
evidence, not master acceptance. The current theorem-DAG projection agrees.
The statement predecessor is therefore not dependency-ordered `[x]`, and this
worker neither redoes nor promotes the item.

The tracked `statement-receipt.json` is historical negative evidence. It has
schema `stage1-node-receipt/1.0`, SHA-256
`80be2de2f421fb2ced32a0d4c3c81aa88e007248977f4e6891c4268b0c70708d`,
Git blob `b02f5ad023212c52c0d10285de3306e8be28dbe4`, `accepted=false`,
`verdict=blocked`, `phase_accepted=false`, no statement fingerprint, and four
unexecuted mutation classes. It binds the earlier base
`dae1951609072752d49d111bf00e78e4512f2d14`, graph digest
`3d32f808e2914b338c459d52651b69731f0979a90a720f98bc0f31a577e2bafa`,
and the then-current `[ ]` statement cursor. It cannot prove the current
positive phase predicate or transfer predecessor/provider acceptance.

## Dependency and reuse audit

The supplied `parent_inspection_order` is exactly `[]`. The direct-hard-parent,
transitive-hard-ancestor, hard-edge, reuse-hint, and shared-group lists are also
exactly empty. The complete required closure was therefore traversed exactly
once as the empty sequence before any Lean replay. No parent phase state,
receipt, declaration body, reusable artifact, terminal proof body, import,
copy, transport, checkbox state, acceptance, or proof credit was consumed or
inherited. No proof work was performed. The empty declared context is not a
claim of mathematical independence.

The tracked `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It binds the same historical base and
obsolete graph digest as the receipt. Validation against the assigned current
graph and worker base fails with
`dependency reuse ledger does not match the graph supplied to its worker`.
It is deliberately not refreshed: a ledger-only rewrite cannot make the
immutable validator replayable and would invalidate the historical receipt's
content bindings.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_semantically_stale_for_current_worker_base`
is the first worker-unrepairable gate. The mandatory HEAD contract has
SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
and Git blob `84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For `statement` it declares:

- `Stage1_Instances/THM-M-0129/check_statement.py`
- `Stage1_Instances/THM-M-0129/check_statement_artifacts.py`

Exactly one candidate exists at the worker base and in the current tree:
`check_statement.py`, SHA-256
`79af4075049bdbde1ea3e1580519e5eac9df414c274074b54f563d8fe1fb6e08`,
Git blob `cc7f95c83d02599804eb6b487cb436601cba8796`. The worktree, HEAD, and
worker-base bytes agree; this worker did not create, refresh, replace, rename,
or delete either candidate. The authority-selected command is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0129/check_statement.py
```

It exited `1`, wrote no stderr, and emitted exactly one 436-byte JSON line
(including its final newline), SHA-256
`f6fd12d153e21fcea837646b9b2b151a572c06bfb993143f10a1f5f3f209e557`:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"S01-ARTIFACTS","item_id":"S56-M-0129-STATEMENT","message":"statement packet check failed: AssertionError: ","open_obligations":1,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0129","verdict":"repair_required"}
```

The stdout is exactly one object with schema
`stage1-validator-semantic-result/1.0`, but its typed semantics are
`status=failed`, `verdict=repair_required`, `phase_accepted=false`, and
`phase_predicate_proven=false`. The immutable validator asserts its historical
base, graph, `[ ]` cursor, historical ledger, and a root worker handoff that is
not part of current HEAD before it can report the historical negative packet.
Exit status, structural checks, or prior self-test prose cannot override this
typed failure. The worker is forbidden to refresh the scheduler-owned
validator, so no current-base phase receipt or self-test handoff can be
truthfully emitted.

## Positive statement gate

Independently of validator freshness, `S02-EXACT-TARGET` and `S03-MUTATIONS`
remain open. Shimura's 1973 Section 3 Main Theorem, Corollary 1.8, Theorem 1.9,
and the corollary following the Main Theorem distribute the construction,
coefficient/eigenvalue, modularity, cuspidality, and Hecke content differently
from the intake's combined modern wording. Selecting only the Main Theorem
narrows the intake; silently conjoining the results invents a new root.
Parameterization, power-of-two normalization, target level and character,
conductor, low-weight cuspidality, Hecke prime range, squarefree admissibility,
and degenerate cases remain theorem-changing open choices.

`Statement.lean` therefore deliberately declares no canonical proposition. Its
two adjacent-interface imports elaborate at trust level zero, while
`StatementInfrastructure.lean` checks ordinary `CuspForm` and
`DirichletCharacter` surfaces and confirms the three topic identifiers
`HalfIntegralWeightModularForm`, `ShimuraLift`, and `ShimuraCorrespondence` are
absent. The historical `S1_M_047.StatementShape` remains excluded because it
stores theorem-critical laws as unconstrained propositions and omits the
squarefree parameter and coefficient equality. These are bounded negative
observations, not an exact target, target-minimal imports, expression or
environment fingerprint, checked transport, or mutation certificate.

## Checks run

All commands ran in this worker clone on 2026-07-17 (Asia/Shanghai). The
automation-provided canonical `.lake` symlink was reused read-only. No
`lake update`, `lake build`, dependency clone/fetch, checkout, network action,
or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Fifteen assurance groups, all 1546 uniform-L0 targets, the v2 DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed relationships, state preservation, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target L0/rework-required manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0129` | 0 | Rank 47, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Candidate enumeration and Git-blob comparison | 0 | Exactly one declared candidate exists, and its worktree, HEAD, and worker-base bytes agree. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0129/check_statement.py` | 1 | Exactly one typed `failed` / `repair_required` object reported `phase_accepted=false`. |
| Current-base ledger validation through `validate_dependency_reuse_ledger` | 1 | Historical ledger does not match the assigned graph/base; it was not credited or rewritten. |
| From `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0129/Statement.lean` | 0 | Declaration-free boundary role elaborated; no exact-target credit. |
| From `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0129/StatementInfrastructure.lean` | 0 | Three adjacent interfaces and three expected-missing identifiers checked; no exact-target credit. |
| Pinned package revision and status checks | 0 | Mathlib is at `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `flt-regular` is at `56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, and both package worktrees are clean. |
| `git diff --check -- Stage1_Instances/THM-M-0129 .stage1-worker-selftest.json` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No handoff exists because the mandatory replay and positive phase predicate did not pass. |

The passing structural and Lean checks are bounded supporting observations.
They do not replace the failed scheduler-selected semantic replay.

## Retry condition and status boundary

The scheduler/master lane must publish a current-authority statement validator
and issue a fresh claim whose base contains the identical unchanged blob. A
fresh worker can then bind the current empty dependency ledger and exactly one
current receipt. Positive closure independently requires dependency-ordered
intake acceptance, lawful preservation and independent approval of one exact
primary result or explicit owned composition, reconciliation of every
theorem-changing convention, a kernel-elaborated exact target with minimal
pinned imports and fingerprints, checked transports, and all four required
mutation classes.

This blocker grants no state transition, phase acceptance, accepted receipt,
exact-statement credit, proof credit, provider acceptance transfer, `AUDIT-Z`,
`THEOREM-Z`, theorem completion, or master acceptance. Because the assigned
phase is not genuinely self-tested at the current base, no
`.stage1-worker-selftest.json` is emitted.
