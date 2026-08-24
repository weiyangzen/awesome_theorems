# Stage2 Catalog Integrity and Isolated Execution Blueprint

> **SUPERSEDED / HISTORICAL — DO NOT EXECUTE**
>
> This is a frozen Stage2 record. Its `[x]` marks only former Stage2 acceptance and satisfies no
> Stage5.1 gate. Do not launch workers or mutate its cursor. The current project SSOT is the
> Stage5.1 organization release and its theorem/conjecture Blueprints.
>
> Document type: former Stage2 execution blueprint retained as historical evidence
>
> Blueprint version: `stage2-catalog-integrity/1.0`
>
> Execution contract: `b3ehive-execution/1.5.0`
>
> Historical source path: `Docs/Stage2_Blueprint.md`
>
> Derived, read-only schedule: `Docs/Stage2_Gantt.md`
>
> State protocol: `[ ]` not done, `[_]` durable worker self-test awaiting Master, `[x]` Master accepted
>
> Initial authority revision: `9c299dbabd34878a420db46ca66d687886fe2b04`

## 0. Mission

Stage2 turns the repository from a broad, weakly typed theorem list plus a legacy Stage1 executor into
an evidence-bound claim catalog with a reproducible Lean 4 validation lane and an isolated execution
controller.

It has four coupled deliverables:

1. install and prove the exact Lean 4 environment required by the tracked project;
2. distinguish theorems, lemmas, conjectures, hypotheses, open problems, laws, models, effects,
   algorithms and non-claim glossary entries without erasing legacy IDs;
3. repair the highest-risk `THM-M-0387` mathematical, provenance and benchmark contracts; and
4. replace the forbidden app-server/shared-state worker transport with task-local tmux, one
   interactive Codex TUI, one authenticated `/goal`, and one private `CODEX_HOME` per claim.

Stage2 does not assert that all 3,338 source rows are true, proved, formalized or benchmark-ready.
It makes those propositions separately testable. It also does not manufacture completion for the
10,822 historical Stage1 phase rows.

## 1. Former Authority and Migration Boundary

This file was the only writable Stage2 requirements and task-state authority. Its checklist is now a
frozen historical cursor and must not be scheduled or mutated. Stage3 may consume an exact Stage2
artifact only when a Stage3 item names that evidence boundary.

The following are inputs or projections, never competing cursors:

| Surface | Stage2 role | Write authority |
|---|---|---|
| `Docs/Stage0_Blueprint.md` | historical generated catalog snapshot | frozen input |
| `Docs/Stage1_Blueprint_v2.md` | historical Stage1 policy/state snapshot | frozen input during migration |
| `Docs/Stage1_*_v2.json` | Stage1 read-only projections | generators only |
| `Docs/researches/*.md` | raw source pools, not verified truth | catalog curation tasks |
| `Docs/Stage2_Gantt.md` | derived schedule projection | generator/Master only; no checkbox state |
| future Stage2 JSON/todo/status files | derived projections | generator only |
| theorem dossiers and receipts | evidence, not progress authority | exact owner plus Master acceptance |

No Stage1 executor or repo-local skill may launch a new worker after this blueprint is accepted until
`S2-EXE-014` quarantines the legacy transport and `S2-EXE-003` through `S2-EXE-006` pass. Existing
Stage1 files remain available for migration evidence; they do not authorize app-server execution.

Only the canonical Master may change a Stage2 mark to `[x]`. A worker never edits this file. The
controller may propose `[ ] -> [_]` only after harvesting a checksum-valid durable handoff. Both
`[ ]` and `[_]` are unfinished and block completion cleanup.

## 2. Frozen Repository-Local Execution Specification

The controller must hash this specification into every claim and ledger. A policy change retires or
migrates old claims; it never silently reinterprets them.

| Field | Frozen Stage2 value |
|---|---|
| canonical repository root | runtime result of `git rev-parse --show-toplevel`; basename is not policy |
| authoritative blueprint | `Docs/Stage2_Blueprint.md` |
| checklist markers | `STAGE2-EXECUTION-CHECKLIST:BEGIN/END` |
| stable item grammar | `S2-(AUTH|ENV|AUD|CAT|M38|EXE|REL)-[0-9]{3}` |
| dependency source | explicit `depends_on=` field on each checklist row |
| runtime root | `.ops/stage2-execution-v1/` |
| task root | `.ops/stage2-execution-v1/tasks/<claim-id>/<run-id>/` |
| queue root | `.ops/stage2-execution-v1/queue/` with immutable checksum-keyed entries |
| selected platform | Codex interactive TUI |
| route policy | installed Codex default unless the operator explicitly freezes model/effort/tier; record resolved route |
| worker transport | task-local tmux server/socket/session + interactive TUI |
| goal protocol | exactly one authenticated active `/goal` per claim |
| Codex state | one private writable `CODEX_HOME` per claim; credentials-only bootstrap |
| forbidden transports | app-server, JSON-RPC worker multiplexing, `codex exec`, shared daemon, shared tmux, no-tmux Codex |
| canonical checkout writer | Master only |
| worker writable scope | exact repository-relative `owned_paths`; authoritative blueprint and canonical checkout forbidden |
| result schema | `stage2-worker-result/1.0` |
| Master receipt schema | `stage2-master-acceptance/1.0` |
| status schema | `stage2-execution-status/1.0` |
| scheduler cadence | two minutes after explicit installation |
| cron marker | `# BEGIN AWESOME_THEOREMS_STAGE2_EXECUTION_V1` / matching END marker |
| scheduler lease | `.ops/stage2-execution-v1/locks/scheduler.lock`; short state transactions only |
| exact-path conflict budget | zero overlapping writable paths among admitted/integrating claims |
| startup hard deadline | 15 minutes from `tmux_started`; override `AT_STAGE2_STARTUP_DEADLINE_SECONDS` |
| goal authentication deadline | 10 minutes from one `goal_submitted`; override `AT_STAGE2_AUTH_DEADLINE_SECONDS` |
| admission-pump budget | 90 seconds per scheduler invocation; override `AT_STAGE2_PUMP_BUDGET_SECONDS` |
| no-progress guard | after three reconciliation iterations inside one admission pump with no state transition, end that invocation and persist the concrete limiter; the next tick may retry after fresh reconciliation; override `AT_STAGE2_NO_PROGRESS_ITERATIONS` |
| claim ledger | `.ops/stage2-execution-v1/ledgers/claims.jsonl`, schema `stage2-claim-ledger/1.0` |
| transition ledger | `.ops/stage2-execution-v1/ledgers/transitions.jsonl`, schema `stage2-transition-ledger/1.0` |
| admission ledger | `.ops/stage2-execution-v1/ledgers/admission.jsonl`, schema `stage2-admission-ledger/1.0` |
| integration ledger | `.ops/stage2-execution-v1/ledgers/integration.jsonl`, schema `stage2-integration-ledger/1.0` |
| cleanup ledger | `.ops/stage2-execution-v1/ledgers/cleanup.jsonl`, schema `stage2-cleanup-ledger/1.0` |
| validate-only output | one JSON object using `stage2-validate-only/1.0`, including resolved defaults, overrides, limits, host observations and zero created claims/processes |
| cleanup policy | controller-owned processes/runtime only; canonical artifacts preserved |

### 2.1 Checklist Parser

Each authoritative item is one physical line with this shape:

```text
- [STATE] `ITEM-ID` title | depends_on=ID,ID-or-- | owned_paths=path,path-or-- | gate=verifiable acceptance sentence
```

`STATE` is exactly one of a single space, underscore or lowercase `x`. Dependencies must exist and
the explicit graph must be acyclic. Document order is presentation order only; it is never a hidden
dependency or global layer barrier.

### 2.2 Ownership

Claims materialize only the declared writable paths and individually justified read-only bootstrap
files, preserving repository-relative names and independent inodes. They must not copy, clone,
archive, mount, rsync, reflink or hardlink the complete repository. A task may use a small Git
baseline containing only its allowed files.

Every claim root has exactly this shape:

```text
.ops/stage2-execution-v1/tasks/<claim-id>/<run-id>/
  work/
  codex-home/
  tmux.sock
  claim.json
  result.json
```

The immutable claim card binds item/claim/run IDs, specification digest, baseline, exact paths,
dependencies, deadline, validation argv, artifact policy, retry budget and canonical checkout as a
forbidden write target. Launch and harvest both verify independent inodes, unchanged claim metadata,
exact ownership and absence of full-checkout sentinel combinations.

### 2.3 Result and Master Schemas

A worker result is provisional and must contain at least:

```json
{
  "schema_version": "stage2-worker-result/1.0",
  "claim_id": "...",
  "run_id": "...",
  "item_id": "...",
  "spec_sha256": "...",
  "baseline": "...",
  "status": "self_tested",
  "changed_paths": [],
  "patch_sha256": "...",
  "commands": [{"argv": [], "cwd": "...", "exit_code": 0, "output_sha256": "..."}],
  "artifacts": []
}
```

A Master receipt additionally binds the immutable handoff checksum, applied paths, dependency and
conflict decision, canonical post-integration tree, repository gates, verdict, timestamp and
reconciled completion surfaces. No receipt may claim an inapplicable test or evidence category.

## 3. Codex Transport and Startup State Machine

The executable controller must freeze and test:

```text
WORKER_TRANSPORT=tmux_codex_tui
WORKER_GOAL_COMMAND=/goal
APP_SERVER_WORKERS=forbidden
CODEX_PROCESS_ISOLATION=one_process_tree_per_claim
CODEX_STATE_ISOLATION=one_writable_home_per_claim
```

It constructs argv as an array and starts one task-local tmux server. The private `CODEX_HOME` gets
only required credentials and minimal explicitly frozen route/provider configuration. It never gets
plugins, marketplaces, MCP configuration, trust history, prior threads/goals/logs or SQLite state.

Startup is durable:

```text
reserved -> materialized -> tmux_started -> goal_pasted -> goal_submitted
         -> live -> handoff_ready -> finished
```

The controller detects the real idle composer, pastes one short `/goal` through a task-local tmux
buffer, appends a claim-specific completion token, and polls joined composer text until that token is
visible. It then submits exactly once. A timeout retires the attempt; it never sprays Enter or resends
the goal. Delayed registry writes may retain a healthy `goal_submitted` lane until its bounded hard
deadline and a later tick may promote it without relaunch.

A lane counts as live only when tmux socket/session, pane PID and start time, cwd, private
`CODEX_HOME`, resolved route, thread registry and exactly one active goal all match the durable claim,
and the goal objective names the item. Process-name counts are telemetry only.

## 4. Admission, Resources and Progress

The requested Stage2 logical ceiling is six concurrent authenticated claims. Six is a ceiling, not a
target that overrides host or dependency gates. Installation is dormant at zero until the transport,
isolation and validation items are Master accepted.

| Limit | Activation value | Rule |
|---|---:|---|
| logical claims | 6 | unique claim identity and task root |
| startup reservations | 4 | includes `reserved` through `goal_submitted` |
| launch fanout per wave | 2 | repeated waves in one tick must be able to reach six |
| authenticated live goals | 6 | exact authenticated liveness only |
| running turns | 6 | separately measured from live idle goals |
| Master integrations | 1 | canonical checkout is single-writer |
| CPU validator leases | 4 | admission recomputes host headroom |
| accelerator leases | 0 | no accelerator requirement discovered |

Host defaults, derived from the observed 32 logical CPUs, 92 GiB RAM and multi-terabyte workspace,
are conservative and operator-reducible: require 16 GiB available RAM, 100 GiB free disk, no active
swap exhaustion and one-minute load below 24 before new admission. Each task is capped at 20 GiB
allocated blocks, 64 MiB controller logs and six hours wall time unless its checklist gate freezes a
smaller budget. Increasing a cap requires an explicit blueprint change and Master validation.

The controller exposes only the following resource override names and reports every resolved value in
validate-only output: `AT_STAGE2_MIN_AVAILABLE_MEMORY_GIB`, `AT_STAGE2_MIN_FREE_DISK_GIB`,
`AT_STAGE2_MAX_LOAD_1M`, `AT_STAGE2_TASK_DISK_GIB`, `AT_STAGE2_TASK_LOG_MIB`,
`AT_STAGE2_TASK_WALL_SECONDS`, plus the deadline/pump/no-progress names frozen in Section 2.
An override may reduce admission or storage; raising a safety ceiling is rejected unless a later
Master-accepted blueprint revision explicitly permits it.

One scheduler invocation uses a bounded admission pump outside the global lease: reconcile, launch
at most two, authenticate, recompute all limiters, then launch the next wave. With six eligible,
conflict-free fixtures and admitted headroom, it must converge to exactly six authenticated lanes in
one invocation. Every missing slot persists a specific dependency, conflict, startup, route,
resource, external-limit, validator or invocation-budget reason.

Status reports separately expose `[ ]`, `[_]`, `[x]`, logical claims, starting lanes, authenticated
goals, running turns, finished handoffs, dependency/conflict/resource/route blocks, integration and
repair backlog, last progress and cleanup state.

## 5. Scheduler, Handoff and Master Integration

Each tick performs short, resumable phases:

1. lock and validate the frozen specification;
2. harvest checksum-valid results into immutable queue storage and stop finished tmux servers;
3. reconcile dead, mismatched, delayed, interrupted and accepted identities;
4. parse checklist/DAG truth and regenerate status;
5. reserve a bounded dependency-ready, exact-path-conflict-free integration/launch set;
6. release the scheduler lock before materialization, TUI startup, network, model work or tests;
7. integrate a bounded batch and pump launch waves outside the lock; and
8. reacquire briefly to merge outcomes, refresh status and schedule scoped cleanup.

Harvest always precedes stale pruning. Finished lanes release live capacity and stop their TUI
immediately. Repair reuses the same task root, thread and active goal as an ordinary follow-up turn;
it never submits a second `/goal`. If repair is requested after that TUI stopped, a new task-local OS
process may reconnect only after authenticating the recorded thread and still-active goal. OS process
identity is deliberately not a repair invariant.

Only the Master applies a queued patch to the preserved canonical checkout, resolves conflicts,
runs item-specific and repository-wide gates, writes `[_]`/`[x]`, checkpoints if policy requires,
and reconciles catalog, receipt, status and Gantt projections. Validation failure preserves the
handoff and moves it to bounded repair without pinning unrelated ready work.

## 6. Repository Acceptance Profiles

Stage2 uses only gates applicable to the item. The current profiles are:

### Blueprint and catalog

```bash
python3 Docs/tools/check_stage2_blueprint.py
python3 Docs/tools/check_stage1_theorem_dag_v2.py
python3 -m unittest scripts/test_stage2_blueprint.py
```

### Python execution controller

```bash
python3 -m py_compile scripts/stage2_execution_cron.py
python3 -m unittest scripts/test_stage2_execution_cron.py
python3 scripts/stage2_execution_cron.py --validate-only --workers 0
```

The Stage2 controller profile becomes required only after its files exist and its checklist item is
integrated. Validate-only must create no claim, tmux server or worker process.

### Lean and `THM-M-0387`

```bash
bash THM-M-0387/run_local_validation.sh
```

The current receipt must bind repository tree, toolchain, manifest dependencies, commands and output
digests. A historical pass is provenance, not a substitute for a current run.

### Hygiene

```bash
git diff --check
git status --short
```

Unrelated user changes are preserved. No gate resets, stashes, checks out, deletes or rewrites them.

## 7. Generated Validation Requirements

Before activation the Stage2 controller tests must prove:

- validate-only launches nothing and creates no claim;
- executable launch surfaces cannot resolve to app-server or `codex exec`;
- each simultaneous claim has a distinct task root, tmux server/socket/session, process identity,
  private writable `CODEX_HOME`, thread and goal;
- exactly one complete `/goal` is submitted per claim;
- only fully authenticated claims count as live;
- delayed authentication promotes without a duplicate launch;
- dead/mismatched startup is released only after its bounded deadline;
- harvest occurs before prune and finished TUI servers stop immediately;
- scheduler lock file descriptors are closed before launch;
- all caps prevent lane seven;
- repeated fanout-two waves reach six admitted live fixture claims in one pump;
- every underfill has a persisted concrete reason;
- changed paths remain within exact ownership and use independent inodes;
- repair stays on the same thread and goal;
- cleanup removes only controller-owned processes/runtime; and
- two unlike fixture repositories leak no project name, path, item prefix, language, validator,
  route or concurrency constants into one another.

Static validation scans executable/config launch surfaces for forbidden transports and generated
artifacts for unexplained absolute paths or cross-fixture tokens. Negative prose in this blueprint is
allowed; executable command-shaped use is not.

## 8. Cleanup and Terminal Condition

Explicit stop removes only the exact Stage2 cron marker, stops each recorded task-local tmux server,
terminates surviving task descendants by recorded PID/start time/cwd/environment, and preserves the
canonical repository plus queued handoffs.

Completion cleanup additionally requires zero `[ ]`, zero `[_]`, no handoff/integration/repair or
checkpoint backlog, every required acceptance profile passing, all completion surfaces reconciled,
and a second scheduler interval proving nothing was recreated. Cleanup is idempotent and verifies
cron lines, scheduler processes, task processes, sockets, locks and runtime roots are absent.

An empty ready frontier, missing evidence, resource pressure, deferred theorem or open conjecture is
not completion.

<!-- STAGE2-EXECUTION-CHECKLIST:BEGIN -->
## 9. Authoritative Stage2 Checklist

- [x] `S2-AUTH-001` Freeze repository evidence, execution-skill version and Stage2 authority boundary | depends_on=- | owned_paths=Docs/Stage2_Blueprint.md | gate=Master confirms the frozen Stage2 predecessor boundary is recorded
- [x] `S2-AUTH-002` Implement the Stage2 blueprint and Gantt structural validator | depends_on=S2-AUTH-001 | owned_paths=Docs/tools/check_stage2_blueprint.py,scripts/test_stage2_blueprint.py | gate=positive and mutation tests prove unique IDs, valid states, dependency closure, acyclicity and exact Gantt projection
- [ ] `S2-AUTH-003` Freeze current branch, dirty-tree, host, process, cron and legacy-runtime inventory | depends_on=S2-AUTH-001 | owned_paths=Docs/evidence/stage2_repository_inventory.json | gate=content-bound inventory records branch/upstream, tracked state, resources and controller-owned versus unrelated processes
- [ ] `S2-AUTH-004` Generate a three-state Stage2 status surface from this checklist | depends_on=S2-AUTH-002,S2-AUTH-003 | owned_paths=Docs/Stage2_Status.json | gate=status reports separate cursor, claim, startup, live, handoff, block, integration and repair counts
- [x] `S2-ENV-001` Install official elan and the tracked Lean 4 toolchain | depends_on=S2-AUTH-001 | owned_paths=Docs/evidence/lean_environment.json | gate=elan, Lean 4.29.0 and Lake versions resolve through the tracked toolchain and are recorded without modifying source pins
- [x] `S2-ENV-002` Materialize the committed Lake dependency closure | depends_on=S2-ENV-001 | owned_paths=Docs/evidence/lean_dependencies.json | gate=mathlib, flt-regular and all transitive package revisions match lake-manifest.json and the lockfile remains unchanged
- [x] `S2-ENV-003` Repair the bootstrap and environment preflight entrypoint | depends_on=S2-ENV-001 | owned_paths=Formalizations/Lean/README.md,THM-M-0387/run_local_validation.sh,scripts/check_lean_environment.py | gate=entrypoint respects ELAN_HOME or elan run, checks exact versions and fails with an actionable structured diagnosis
- [x] `S2-ENV-004` Run the complete M0387 validation against the current tree | depends_on=S2-ENV-002,S2-ENV-003 | owned_paths=THM-M-0387/build_validation.md,THM-M-0387/meta.json,THM-M-0387/receipts/current-validation.json | gate=seven-stage command succeeds and receipt binds Git tree, pins, argv, exit codes and output hashes
- [ ] `S2-ENV-005` Prove cold fresh-clone replay in an isolated home and empty cache | depends_on=S2-ENV-004 | owned_paths=THM-M-0387/receipts/cold-replay.json | gate=independent clean replay succeeds without lock drift and records network, disk, wall-time and artifact identities
- [x] `S2-AUD-001` Complete six-view critical audit of THM-M-0387 | depends_on=S2-AUTH-001 | owned_paths=Docs/reviews/THM-M-0387_Critical_Audit_2026-08-10.md | gate=report separates confirmed strengths, P0/P1/P2 defects and executable acceptance gates with repository evidence
- [x] `S2-AUD-002` Complete six-view PutnamBench and scientific-benchmark audit of the THM lists | depends_on=S2-AUTH-001 | owned_paths=Docs/reviews/THM_List_Benchmark_Audit_2026-08-10.md | gate=report gives reproducible statistics and concrete math, physics and CS record defects plus benchmark comparables
- [x] `S2-AUD-003` Complete six-view catalog, conjecture and ID audit | depends_on=S2-AUD-002 | owned_paths=Docs/reviews/THM_Catalog_and_ID_Audit_2026-08-10.md | gate=report proposes evidence-backed claim-kind completion, stable IDs, aliases and migration rules without erasing legacy identity
- [x] `S2-CAT-001` Freeze all 3338 raw source records with source locators | depends_on=S2-AUD-002 | owned_paths=Docs/catalog/Source_Records_v2.json | gate=every parsed row has source path, section, ordinal and byte-stable source locator with no silent loss
- [x] `S2-CAT-002` Define the canonical claim-record schema | depends_on=S2-AUD-003 | owned_paths=Docs/catalog/Claim_Record_Schema_v2.json | gate=schema separates identity, claim kind, exact statement, human status, formal status, repo status, provenance, license and benchmark policy
- [x] `S2-CAT-003` Separate human, formal-system, repository and benchmark status axes | depends_on=S2-CAT-002 | owned_paths=Docs/catalog/Status_Taxonomy_v2.md | gate=no migrated value can collapse mathematical truth, published proof, external formal proof, local replay and benchmark release into one label
- [x] `S2-CAT-004` Create an immutable legacy-to-canonical ID registry | depends_on=S2-CAT-001,S2-CAT-002 | owned_paths=Docs/catalog/Claim_ID_Registry_v2.json | gate=all legacy THM IDs resolve exactly once while typed canonical IDs remain stable across reorder and source insertion
- [x] `S2-CAT-005` Record duplicate, alias, refinement and same-name-different-claim relations | depends_on=S2-CAT-004 | owned_paths=Docs/catalog/Claim_Relations_v2.json | gate=all 76 removed rows and detected cross-record collisions have typed, reviewable relations rather than destructive deduplication
- [ ] `S2-CAT-006` Repair the mathematics claim-kind and statement sample | depends_on=S2-CAT-002,S2-AUD-003 | owned_paths=Docs/catalog/repairs/Mathematics_v2.json | gate=audited theorem, lemma, conjecture, hypothesis and open-problem records have exact domains, hypotheses and source boundaries
- [ ] `S2-CAT-007` Repair the physics claim-kind and regime sample | depends_on=S2-CAT-002,S2-AUD-003 | owned_paths=Docs/catalog/repairs/Physics_v2.json | gate=laws, models, effects and empirical relations are not mislabeled as universal theorems and include regime, units, approximation and observables
- [ ] `S2-CAT-008` Repair the computer-science claim-kind and model sample | depends_on=S2-CAT-002,S2-AUD-003 | owned_paths=Docs/catalog/repairs/Computer_Science_v2.json | gate=audited records freeze computation model, encoding, reduction, resource bound, probability and adversary assumptions where applicable
- [ ] `S2-CAT-009` Add source, license, copyright and redistribution records | depends_on=S2-CAT-001,S2-CAT-002 | owned_paths=LICENSE,NOTICE,Docs/catalog/Provenance_and_License_v2.json | gate=each distributable task component has SPDX and immutable provenance or is explicitly citation-only
- [ ] `S2-CAT-010` Define versioned benchmark task tracks and scorer contract | depends_on=S2-CAT-002,S2-AUD-002 | owned_paths=Docs/catalog/Benchmark_Task_Schema_v2.json,Docs/catalog/Benchmark_Protocol_v2.md | gate=statement, proof, retrieval, audit and open-challenge tracks have distinct inputs, outputs, resources, metrics and negative fixtures
- [ ] `S2-CAT-011` Assign family-safe split, leakage and answer-visibility policy | depends_on=S2-CAT-004,S2-CAT-005,S2-CAT-010 | owned_paths=Docs/catalog/Benchmark_Splits_v2.json | gate=aliases, equivalent statements and shared proof families cannot cross splits and public contaminated tasks never enter held-out aggregate score
- [ ] `S2-CAT-012` Generate the complete canonical catalog and projections | depends_on=S2-CAT-003,S2-CAT-004,S2-CAT-005,S2-CAT-006,S2-CAT-007,S2-CAT-008,S2-CAT-009 | owned_paths=Docs/tools/generate_claim_catalog_v2.py,Docs/catalog/Claim_Catalog_v2.json,Docs/catalog/Claim_Catalog_v2.md | gate=generation is deterministic, lossless and schema-valid and leaves raw sources plus legacy Stage0 untouched
- [ ] `S2-CAT-013` Add catalog mutation, coverage and ID-stability tests | depends_on=S2-CAT-012 | owned_paths=scripts/test_claim_catalog_v2.py | gate=tests reject dropped rows, duplicate IDs, unstable reorder, invalid aliases, collapsed status axes and incomplete conjecture fields
- [ ] `S2-M38-001` Repair WTW exponent typing, 2-adic normalization and residual case split | depends_on=S2-AUD-001 | owned_paths=THM-M-0387/readable/wiles_taylor_wiles_process.md,THM-M-0387/proof_units.json | gate=pF and r are distinct typed parameters, local invariants are explicit and all residual cases are exhaustive
- [ ] `S2-M38-002` Repair regular Case II residue-map and induction semantics | depends_on=S2-AUD-001 | owned_paths=THM-M-0387/eligibles/regular_primes_proof_process.md,THM-M-0387/proof_units.json,THM-M-0387/full_study.md | gate=normalized residue map and eta-zero match pinned source and formal ledgers mirror natural-number induction rather than a fictitious minimal witness
- [ ] `S2-M38-003` Repair n3 and n4 readable dependency and side-condition chains | depends_on=S2-AUD-001 | owned_paths=THM-M-0387/eligibles/n3_proof_process.md,THM-M-0387/eligibles/n4_proof_process.md,THM-M-0387/proof_units.json | gate=conditional reductions, Solution conversions, PID-UFD inputs, signed squares and nonzero conditions match pinned theorem order
- [ ] `S2-M38-004` Bind the canonical Statement directly to pinned mathlib | depends_on=S2-ENV-002,S2-AUD-001 | owned_paths=Stage1_Instances/THM-M-0387/Statement.lean,Stage1_Instances/THM-M-0387/Proof.lean,Stage1_Instances/THM-M-0387/check_statement.py | gate=one imported target is kernel-related to actual Mathlib FermatLastTheorem and Proof cannot redefine it
- [ ] `S2-M38-005` Probe every public wrapper and each consumed upstream terminal | depends_on=S2-ENV-002,S2-AUD-001 | owned_paths=scripts/lint_theorem_dossier.py,THM-M-0387/proof_units.json,THM-M-0387/machine_checked_audit.md | gate=enumerated public declarations and upstream terminals have exact types, axiom sets, source identities and checked wrapper links
- [ ] `S2-M38-006` Replace string-only and false-zero validation gates | depends_on=S2-M38-004,S2-M38-005 | owned_paths=Stage1_Instances/THM-M-0387/check_intake.py,Stage1_Instances/THM-M-0387/check_validation.py,Stage1_Instances/THM-M-0387/validation-spec.json | gate=declared recipes execute, semantic failures exit nonzero and positive plus adversarial fixtures pass
- [ ] `S2-M38-007` Version the 132-node evidence snapshots and crosswalk | depends_on=S2-AUD-001 | owned_paths=THM-M-0387/evidence-manifest.json,Stage1_Instances/THM-M-0387/obligation-crosswalk.json | gate=historical and current nodes carry snapshot, namespace, denominator and derivation hashes with one-to-one reviewed mapping
- [ ] `S2-M38-008` Publish an honest M0387 benchmark manifest | depends_on=S2-CAT-010,S2-CAT-011,S2-M38-004,S2-M38-006 | owned_paths=THM-M-0387/benchmark-task.json,THM-M-0387/DATASET_CARD.md | gate=tracks, contamination, open-root exclusion, allowed premises, scorer, licenses and resource budgets are explicit and machine-valid
- [ ] `S2-EXE-001` Persist the frozen Stage2 execution specification digest | depends_on=S2-AUTH-002,S2-AUTH-003 | owned_paths=Docs/Stage2_Execution_Spec.json | gate=generated spec exactly reproduces Section 2 and binds parser, paths, schemas, gates, caps, cadence and cron marker
- [ ] `S2-EXE-002` Implement exact-path task materialization and boundary validation | depends_on=S2-EXE-001 | owned_paths=scripts/stage2_execution_cron.py | gate=fixtures prove declared independent files only, reject full checkout sentinels and keep changes inside ownership
- [ ] `S2-EXE-003` Implement one task-local tmux Codex TUI per claim | depends_on=S2-EXE-002 | owned_paths=scripts/stage2_execution_cron.py | gate=each fixture claim has a unique server, socket, session, process tree, cwd and private CODEX_HOME with no fallback
- [ ] `S2-EXE-004` Implement the exactly-once goal paste and submit handshake | depends_on=S2-EXE-003 | owned_paths=scripts/stage2_execution_cron.py | gate=completion-token proof precedes one submit and partial, timeout or duplicate-goal fixtures fail closed
- [ ] `S2-EXE-005` Implement authenticated liveness and delayed-start promotion | depends_on=S2-EXE-004 | owned_paths=scripts/stage2_execution_cron.py | gate=only exact process-route-thread-goal identity is live and healthy delayed registration promotes without relaunch
- [ ] `S2-EXE-006` Implement resource-aware six-lane admission pumping | depends_on=S2-EXE-005 | owned_paths=scripts/stage2_execution_cron.py | gate=fanout-two waves reach exactly six admitted live fixtures, never seven, and persist every underfill reason
- [ ] `S2-EXE-007` Implement harvest-before-prune immutable handoff queue | depends_on=S2-EXE-002,S2-EXE-005 | owned_paths=scripts/stage2_execution_cron.py | gate=valid result and patch are checksum archived before pruning and finished transports release capacity immediately
- [ ] `S2-EXE-008` Implement dependency-ready conflict-safe Master integration | depends_on=S2-EXE-006,S2-EXE-007 | owned_paths=scripts/stage2_execution_cron.py | gate=single-writer integration preserves dirty canonical work, validates applicable gates and is the only path to x
- [ ] `S2-EXE-009` Implement bounded same-thread same-goal repair | depends_on=S2-EXE-008 | owned_paths=scripts/stage2_execution_cron.py | gate=repair reuses claim root, thread and active goal, permits authenticated process reconnect after harvest, and cannot submit a second goal
- [ ] `S2-EXE-010` Implement short leases and crash-resumable scheduler phases | depends_on=S2-EXE-006,S2-EXE-007,S2-EXE-008 | owned_paths=scripts/stage2_execution_cron.py | gate=no slow launch, network, model, build, test or integration validation holds the global scheduler lock
- [ ] `S2-EXE-011` Implement exact-marker stop and completion cleanup | depends_on=S2-EXE-009,S2-EXE-010 | owned_paths=scripts/stage2_execution_cron.py | gate=cleanup is idempotent, scoped to recorded task identity and refuses completion while any unfinished surface remains
- [ ] `S2-EXE-012` Implement status, todo and evidence ledgers | depends_on=S2-AUTH-004,S2-EXE-010 | owned_paths=scripts/stage2_execution_cron.py,Docs/tools/generate_stage2_status.py | gate=derived outputs expose all cursor, lane, handoff, block and integration dimensions without claiming reservations are live
- [ ] `S2-EXE-013` Add transport, admission, portability and cleanup fixture suites | depends_on=S2-EXE-011,S2-EXE-012 | owned_paths=scripts/test_stage2_execution_cron.py,scripts/fixtures/stage2_execution | gate=all Section 7 positive and negative invariants pass for two unlike fixture repositories
- [ ] `S2-EXE-014` Quarantine the legacy app-server executor and migrate durable evidence | depends_on=S2-EXE-013 | owned_paths=scripts/stage1_execution_cron.py,scripts/stage1_app_server_client.py,skills/execute-stage1-v2/SKILL.md | gate=no current launcher can reach forbidden transport and retained Stage1 evidence remains read-only and content-addressed
- [ ] `S2-REL-001` Reconcile Stage2 blueprint, Gantt, catalog, receipts and status | depends_on=S2-CAT-013,S2-M38-008,S2-EXE-014,S2-ENV-005 | owned_paths=Docs/Stage2_Gantt.md,Docs/Stage2_Status.json,README.md | gate=all public completion surfaces derive from accepted authority and show identical IDs, counts, versions and status boundaries
- [ ] `S2-REL-002` Run the complete repository acceptance matrix twice | depends_on=S2-REL-001 | owned_paths=Docs/evidence/stage2_release_validation.json | gate=two independent clean runs pass blueprint, catalog, controller, Lean, hygiene and deterministic-regeneration gates
- [ ] `S2-REL-003` Perform requirement-by-requirement independent release review | depends_on=S2-REL-002 | owned_paths=Docs/reviews/Stage2_Release_Review.md | gate=review maps every mission requirement and checklist item to direct authoritative evidence and finds no unresolved gate
- [ ] `S2-REL-004` Install the exact Stage2 cron entry | depends_on=S2-REL-003 | owned_paths=- | gate=operator-authorized exact marker is installed once, validate-only remains side-effect free and first tick records dormant-to-active transition
- [ ] `S2-REL-005` Prove terminal cleanup after all work is accepted | depends_on=S2-REL-004 | owned_paths=Docs/evidence/stage2_cleanup.json | gate=zero unfinished or queued work remains and exact scoped cleanup proves cron, processes, sockets, locks and runtime roots absent

<!-- STAGE2-EXECUTION-CHECKLIST:END -->

## 10. Definition of Stage2 Success

Stage2 is complete only when every authoritative row is `[x]`, both catalog and Lean claims are
truthful at their exact evidence boundaries, the forbidden executor is unreachable, the isolated
controller passes all generated tests, the same-name Gantt and status projections reconcile, and
completion cleanup succeeds without touching unrelated host state or canonical accepted artifacts.

Until then this blueprint remains active even if no claim is dependency-ready.
