# THM-M-0121 anchor-audit scheduler blocker

Item: `S56-M-0121-ANCHOR_AUDIT`

Theorem: `THM-M-0121`

Claim order: `(v2_execution_rank=274, phase_layer=2, phase_item_id=S56-M-0121-ANCHOR_AUDIT)`

Worker base revision: `fe1ec5161fd86894fef54d2a1860437053d9e8d7`

Worker base tree: `3777ff4ba4b38bc02217f033c19d32763d75d039`

Worker verdict: `blocked`

Proposed state: `[ ]` (unchanged)

Phase accepted: `false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The mandatory phase contract is `Docs/Stage1_Phase_Acceptance_Contracts.json`, SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`, Git blob
`84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For `anchor_audit` it declares these two
scheduler-owned candidate paths after substituting the theorem ID:

- `Stage1_Instances/THM-M-0121/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0121/check_anchor.py`

Neither path exists in the immutable worker base, the base Git tree, or the current worker tree.
The eligible validator count is therefore zero. The contract requires exactly one candidate,
requires it to exist at the worker base, and requires its HEAD blob to equal its worker-base blob.
The assignment expressly forbids this worker from creating, refreshing, renaming, replacing, or
deleting either candidate.

Consequently the required argv cannot be run and the required stdout, exactly one JSON object with
schema `stage1-validator-semantic-result/1.0`, cannot be obtained. A structural checker, Lean
elaboration, prose report, exit code zero, statement validator, or undeclared adapter cannot stand
in for scheduler-owned semantic replay. Per the explicit zero-or-multiple-candidate rule, this run
creates no anchor inventory, discovery-evidence packet, phase receipt, `AnchorAudit.lean`, or
`.stage1-worker-selftest.json`.

The independent topology gate is also not ready for master closure. The sole intra-theorem
predecessor, `S56-M-0121-STATEMENT`, is authoritatively `[_]`, not master-accepted `[x]`. Its current
receipt reports a truthful blocked statement predicate because no exact source proposition has been
selected. That does not repair or supersede the earlier authority-replay failure.

## DAG and dependency-reuse audit

The task-state authority records the assigned node as `[ ]`, attempt 0, dependent on
`S56-M-0121-STATEMENT`, with the sole owned path `Stage1_Instances/THM-M-0121`. The claim tuple above
follows the mandatory order `(v2_execution_rank, phase_layer, phase_item_id)`.

The authoritative theorem DAG has SHA-256
`6d0668e741eb7f886c28ad37c524f11eb902f5be610ea4e69a68badb80075b39`; the target's stable
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete `parent_inspection_order`, direct-parent list, transitive-ancestor list, hard-edge
list, reuse-hint list, and shared-group list are all `[]`. The exact ordered closure was traversed
once as the empty sequence before any proof work. Zero provider theorems, phase states, receipts,
declarations, bodies, imports, copies, or transports were available to inspect or consume. No proof
work was performed, no provider acceptance was inherited, and the empty graph context is not an
independent mathematical-proof claim.

The tracked `dependency-reuse-ledger.json` already uses schema
`stage1-dependency-reuse-ledger/1.1` and records the correct empty context, but it binds an older
graph digest, repository revision, statement-layer claim tuple, and pending statement receipt. It
is not rewritten in this blocked run: changing that shared target-owned prior-phase input cannot
manufacture scheduler authority and would stale existing content bindings. A fresh executable
anchor claim must refresh it to that claim's graph, base, layer, and item before proof work or a
phase handoff.

## Bounded immutable observations

The following observations are read-only guidance. They are not the contract's precommitted,
content-bound, semantically replayed seven-lane discovery inventory, and they receive no phase or
proof credit.

- The source statement remains unresolved. Repository metadata supplies the label "Mori
  rationality theorem", Mori attribution, a year, and the gloss "rationality of Fano varieties",
  but no immutable theorem passage or exact proposition. Nef-threshold rationality, rational curves
  or uniruledness, rational connectedness, and birational rationality are materially different.
  The unqualified assertion that every Fano variety is rational is false.
- The repo-local legacy source
  `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_040.lean` is Git blob
  `a5895844464dd400fcdb58c2b8f207ae1ac1e78a`, SHA-256
  `327fabea1a35f1dd6bf0c7db33a86518cbf50a046fa3f52cec963f2eef8351f3`. It elaborates in the pinned
  environment and contains genuine rational-map wrappers and explicit missing-API classifications.
  Its root shape leaves the Fano hypothesis and conclusion as predicates, deliberately selects no
  theorem reading, and contains no terminal Mori proof. It is `M3` interface/discovery material,
  not an exact root candidate; legacy status transfers no acceptance.
- The materialized mathlib checkout is exactly revision
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
  `bdc39a3123201dae413a9d9be56ec242c19e5c2b`, with a clean tracked worktree. The adjacent
  `Mathlib/AlgebraicGeometry/RationalMap.lean` source is Git blob
  `4ecab327a4480ac74750aa073e2d8124edccb21a`, SHA-256
  `e6de15c0db2a37ca0455976b8e4fd736b9298adc36537daeff06d924c67301ae`. Exact-topic scans over the
  pinned mathlib source and all eleven materialized Lake packages found no Lean declaration for
  Mori rationality, a nef-threshold theorem, Fano rationality, uniruledness, or rational
  connectedness. The mathlib `docs/1000.yaml` row titled "Rationality theorem" names no declaration.
  These are bounded immutable local results, not global absence.
- No immutable official Lean project, other public Lean 4 project, statement-only collection,
  historical or other-prover snapshot, or primary-source passage was supplied for replay. Network
  access is denied. Those lanes remain unexecuted rather than being misreported as exhaustive
  negative searches.

No observation establishes `M0-L`, `M0-W`, `M0-P`, or `M1`. The honest root remains `H3/M4/R4`,
and no H0, R0, `AUDIT-Z`, `THEOREM-Z`, or theorem completion follows.

## Commands and exact results

All commands ran in this worker clone without fetching, updating, or otherwise mutating `.lake`.

| Command | Exit | Result boundary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 theorem DAG, seven-phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 blueprint states, 2 hard edges, 5 hints, 311 shared groups, acyclic. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | Rank 40, planned, legacy artifacts unaccepted, theorem incomplete. |
| base-tree and worker-tree checks for both declared anchor validators | 0 | Expected blocker assertion passed: eligible candidate count is zero. |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0121/Statement.lean` | 0 | The adjacent rational-map vocabulary probe elaborated; it declares no canonical target or proof. |
| from `Formalizations/Lean`: `env LEAN_NUM_THREADS=1 LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_040.lean` | 0 | The legacy interface and rational-map wrappers elaborated; no exact-root credit follows. |
| pinned mathlib revision, tree, status, source hashes, and bounded exact-topic scans | 0 | Pins and bytes matched; only adjacent substrate and an unbound documentation title were found. |
| `git diff --check -- Stage1_Instances/THM-M-0121 .stage1-worker-selftest.json` | 0 | No whitespace errors in the target-scoped blocker. |

The Lean invocations emit non-fatal sandbox stream-fd diagnostics before normal output. Their zero
exits validate only the scoped elaboration observations above. They are not the missing semantic
anchor validator and cannot imply `phase_accepted`.

## Retry condition and status boundary

The scheduler must commit exactly one declared anchor validator and issue a fresh claim whose base
contains the identical blob. The statement predecessor must separately become master-accepted `[x]`
with an exact, source-faithful proposition before this phase can pass topology and exact statement
normalization. A fresh worker must then refresh the empty schema-1.1 ledger, precommit and execute
all seven ordered discovery lanes, content-bind each candidate, negative result, and access failure,
classify the complete frozen inventory, create exactly one contract-selected phase receipt, and run
the unchanged validator at the contract argv.

This target-scoped blocker grants no phase transition, receipt, source acceptance, proof credit,
audit completion, theorem completion, provider acceptance, or master acceptance. The authoritative
item remains `[ ]`, and no worker self-test handoff is present.
