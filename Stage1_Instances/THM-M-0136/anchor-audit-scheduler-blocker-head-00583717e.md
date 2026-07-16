# THM-M-0136 anchor-audit scheduler blocker

Item: `S56-M-0136-ANCHOR_AUDIT`

Worker base: `00583717e4a5f73f89f5ffee33343caf65cc9721` (tree
`9f2ff1432d1b90ade32db3437fd531e38b49dcf3`)

Claim order: `(v2 rank 286, phase layer 2, S56-M-0136-ANCHOR_AUDIT)`

Verdict: `blocked`; state remains `[ ]`; `phase_accepted=false`

## First failed gate

`G05-AUTHORITY-REPLAY.validator_requires_exactly_one_unchanged_HEAD_candidate_present_at_worker_base`

The HEAD anchor-audit contract declares these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0136/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0136/check_anchor.py`

Neither exists in the worker-base commit or the worktree. The contract requires
exactly one candidate already present at the base and requires its HEAD blob to
remain unchanged. This worker is forbidden to create, refresh, rename, replace,
or delete either path. Therefore there is no lawful validator argv or exact
`stage1-validator-semantic-result/1.0` output for a phase receipt. An undeclared
adapter, prose, or an unrelated exit-zero command cannot repair scheduler
ownership.

The topology gate is independently open: `S56-M-0136-STATEMENT` is `[_]`, not
master-accepted `[x]`, and its receipt reports a blocked, underdetermined exact
statement.

## Dependency audit

The authoritative theorem-DAG SHA-256 is
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`;
the target context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
Direct hard parents, transitive hard ancestors, hard edges, reuse hints, shared
groups, and `parent_inspection_order` are all empty. That complete empty order
was traversed exactly once before any possible proof work. No proof work was
performed, no provider artifact exists to inspect or reuse, and no checkbox,
receipt, acceptance, or proof credit transfers.

The tracked schema-1.1 `dependency-reuse-ledger.json` records the truthful empty
closure, but it binds an older graph and repository revision. It is not refreshed
in this ineligible run: changing the ledger alone cannot manufacture the missing
scheduler replay or a valid self-test packet.

## Scoped observations

The target still names a subject rather than one proposition. The target-owned
`Statement.lean` checks only `Matrix.ToLieAlgebra`,
`CartanMatrix.Generators`, and `CartanMatrix.Relations.toIdeal`. The legacy
`S1_M_052.lean` file has an explicitly provisional matrix-recovery
`StatementShape`; its checked Serre-construction and finite-root-system wrappers
are adjacent infrastructure, not a Kac-Moody classification theorem. Pinned
mathlib contains construction and relation infrastructure but no inspected exact
terminal declaration for the unresolved root.

These are bounded discovery observations, not the required precommitted and
content-bound seven-lane inventory. They supply no H0, M0, R0, root proof, audit
completion, or theorem completion.

## Validation

The standard, v2 DAG, phase-contract, target-manifest, and target-show checks all
exit `0` at the untouched base. Read-only `lake env lean --trust=0` elaboration of both
`Stage1_Instances/THM-M-0136/Statement.lean` and
`AwesomeTheorems/Stage1/S1_M_052.lean` also exits `0`; those checks cover only
their narrow interface and provisional legacy declarations. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

After these two target-owned blocker files were added, the standard and theorem-
DAG checks exit `1` because fresh deterministic evidence inventory differs from
the checked-in read-only theorem-DAG projection. This is the expected integration
boundary: this worker did not edit the forbidden projection, and the scheduler
must regenerate it when integrating the owned evidence.

## Retry condition

The scheduler must publish exactly one declared anchor-audit validator, then
issue a fresh claim whose base already contains that identical blob. A fresh
eligible worker can refresh the empty dependency ledger to that graph/base,
precommit and execute all seven ordered discovery lanes, bind every immutable
result or access failure, classify the frozen inventory, emit exactly one phase
receipt, and replay the unchanged validator. The statement predecessor must
separately become `[x]` before anchor-audit master acceptance.

Per the explicit zero-candidate rule, this run emits no
`.stage1-worker-selftest.json` and no `anchor-audit-receipt.json`. This blocker
changes no task state and claims no phase acceptance, provider acceptance,
proof credit, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or master acceptance.
