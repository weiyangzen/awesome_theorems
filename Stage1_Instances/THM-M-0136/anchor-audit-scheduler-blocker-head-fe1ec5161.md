# THM-M-0136 anchor-audit scheduler blocker

Item: `S56-M-0136-ANCHOR_AUDIT`

Worker base: `fe1ec5161fd86894fef54d2a1860437053d9e8d7` (tree
`3777ff4ba4b38bc02217f033c19d32763d75d039`)

Claim order: `(v2 rank 286, phase layer 2, S56-M-0136-ANCHOR_AUDIT)`

Verdict: `blocked`; state remains `[ ]`; `phase_accepted=false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The HEAD anchor-audit contract declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0136/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0136/check_anchor.py`

Neither exists in the worker-base commit or worktree. The candidate count is
zero. This worker may not create, refresh, rename, replace, or delete either
path. Consequently there is no lawful validator argv or exact
`stage1-validator-semantic-result/1.0` stdout to bind in a phase receipt.
An undeclared adapter, prose report, or unrelated exit-zero command cannot
satisfy scheduler ownership.

The topology gate is independently open. `S56-M-0136-STATEMENT` is `[_]`, not
master-accepted `[x]`, and its receipt reports `accepted=false`, `blocked`, and
`phase_accepted=false` because no exact source-faithful proposition or preserved
equivalence structure is identified.

## Dependency audit

The current theorem-DAG SHA-256 is
`6d0668e741eb7f886c28ad37c524f11eb902f5be610ea4e69a68badb80075b39`;
the target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
Direct hard parents, transitive hard ancestors, hard edges, reuse hints, shared
groups, and `parent_inspection_order` are all empty. The required traversal was
therefore the empty traversal, performed exactly once before any possible proof
work. No provider declaration, receipt, body, import, copy, or transport exists
to inspect or reuse, and no checkbox, acceptance, or evidence credit transfers.

The tracked schema-1.1 `dependency-reuse-ledger.json` truthfully records that
empty closure but binds an older graph and repository revision. It is not
refreshed in this ineligible run: a ledger-only rewrite cannot manufacture the
missing scheduler replay or a valid self-test handoff.

## Scoped observations

The target still names a subject rather than one proposition. The target-owned
`Statement.lean` checks only `Matrix.ToLieAlgebra`,
`CartanMatrix.Generators`, and `CartanMatrix.Relations.toIdeal`. The repo-local
legacy `S1_M_052.lean` has an explicitly provisional matrix-recovery
`StatementShape` and a bounded 2026-05-01 public-search record that reports no
terminal Lean 4 Kac-Moody classification theorem. Pinned mathlib at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies Serre construction and
adjacent Kac-Moody infrastructure, not an inspected exact terminal declaration
for the unresolved root.

Trust-zero elaboration of both Lean files succeeds. This proves only their
narrow interface and legacy gate declarations. It supplies no canonical
statement, terminal proof body, H0, M0, R0, audit completion, or theorem
completion.

## Validation boundary

Before adding this owned blocker, the standard, theorem-DAG, phase-contract,
target-manifest, and target-show checks all exited `0`. Read-only commands were:

- `python3 Docs/tools/check_stage1_standard.py`
- `python3 Docs/tools/check_stage1_theorem_dag_v2.py`
- `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py`
- `python3 scripts/stage1_target.py check`
- `python3 scripts/stage1_target.py show THM-M-0136`
- `cd Formalizations/Lean && LC_ALL=C LANG=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0136/Statement.lean`
- `cd Formalizations/Lean && LC_ALL=C LANG=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_052.lean`

The canonical `.lake` path is an automation-provided untracked symlink. This
worker did not run `lake update`, `lake build`, dependency clone/fetch, or any
command that mutates it.

Adding target-owned evidence changes the theorem DAG's generated evidence
inventory. The worker will not edit that forbidden projection; scheduler
integration must regenerate it.

## Retry condition

The scheduler must publish exactly one declared anchor-audit validator and
restart this task from an authoritative base containing the identical blob. A
fresh eligible worker can then refresh the empty dependency ledger, precommit
and execute all seven ordered discovery lanes, content-bind every immutable
result or access failure, classify the complete inventory, emit exactly one
phase receipt, and replay the unchanged validator. The statement predecessor
must separately become `[x]` before anchor-audit master acceptance.

Per the explicit zero-candidate rule, this run emits no
`.stage1-worker-selftest.json` and no `anchor-audit-receipt.json`. It changes no
task state and claims no phase acceptance, proof credit, provider acceptance,
`AUDIT-Z`, `THEOREM-Z`, theorem completion, or master acceptance.
