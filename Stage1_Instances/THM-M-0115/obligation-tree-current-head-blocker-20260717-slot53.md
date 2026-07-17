# THM-M-0115 obligation-tree current-HEAD blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0115-OBLIGATION_TREE` at worker base
`e19e77ec08fca6a8a9c45a003c9904020dae8382` (tree
`53ff0ebe013670fc0332bf326fd860b29857ddab`). The exact claim tuple is
`(v2_execution_rank=260, phase_layer=3,
phase_item_id=S56-M-0115-OBLIGATION_TREE)`. The sole task-state authority
records the item as `[_]` with one attempt, and its anchor-audit predecessor is
also only `[_]`, not master-accepted.

This continuation changes no theorem statement, registry, typed graph, Lean
composition source, canonical dependency ledger, phase receipt, validator,
task-state authority, or theorem-DAG projection. It emits no worker self-test
handoff because the mandatory semantic replay is negative.

## Dependency Audit

The authoritative theorem DAG has SHA-256
`53622c848d6a0d8327bba8cd22bf45463f0dd8acb7ea0af2884713983e76c91f`,
and the stable dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
The complete `parent_inspection_order` is exactly empty. It was traversed
exactly once before any possible proof work. Direct parents, transitive
ancestors, hard edges, reuse hints, and shared groups are all empty. No
provider state, receipt, declaration, reusable bytes, terminal proof body,
checkbox, proof credit, or acceptance was consumed or inherited.

The canonical schema-1.1 `dependency-reuse-ledger.json` still records that
empty context, but a later integrated proof worker changed its item owner to
`S56-M-0115-PROOF`, layer 4, base `307c34d30...`, and theorem-DAG digest
`8be71ef1...`. Overwriting the sole canonical path with a current layer-3
ledger would invalidate the later proof receipt and would not repair the
immutable validator. This blocker records the assigned empty audit without
misrepresenting or destroying later evidence.

## Preserved Architecture

The integrated architecture is byte-stable and substantial:

- `obligation-registry.json` freezes 32 status-independent obligations under
  denominator `f1455869...`, covering every mandatory `S/N/B/C/L/X/T` layer.
- `typed-graphs.json` contains seven distinct graph families and 192 typed
  edges, three conditional Lean composition certificates, eleven explicitly
  unverified decompositions, and no accepted closed obligation.
- `obligation-tree.md` supplies the mandatory readable layers, substantive
  step ledgers, and open-boundary sentences.
- `ObligationTree.lean` elaborates its three conditional composers under
  `--trust=0`; each reports exactly `propext`, `Classical.choice`, and
  `Quot.sound`, with no `sorryAx`. Its output SHA-256 is `094da5e8...`.

These checks prove that the historical architecture bytes remain coherent.
They do not inhabit a mathematical premise, close any obligation, establish a
terminal proof body, or refresh the current phase receipt. The root remains
`H4/M3/R4`; `audit_complete=false` and `theorem_complete=false`.

## First Failed Gate

The HEAD phase contract declares two scheduler-owned validator candidates and
exactly one exists at this immutable worker base:

```text
Stage1_Instances/THM-M-0115/check_obligation_tree.py
```

Its SHA-256 is
`d9efb330e90f9c81fb43e1a2c14a0d97242bd3d85f43d8f38bd72bad32c19aef`
and its Git blob is `9d4a153e51423864b20c243c2b078929b4e03627`.
The worker did not create, refresh, rename, replace, or delete either declared
candidate.

The exact contract-selected argv was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0115/check_obligation_tree.py
```

It exited zero with empty stderr and exactly one
`stage1-validator-semantic-result/1.0` object:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"G09-FRESHNESS","item_id":"S56-M-0115-OBLIGATION_TREE","message":"one or more frozen authority inputs changed","open_obligations":1,"phase":"obligation_tree","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":["Docs/Stage1_Theorem_DAG_v2.json"],"status":"stale","theorem_complete":false,"theorem_id":"THM-M-0115","verdict":"repair_required"}
```

Exit zero is not phase acceptance. The validator immutably binds old base
`c5037228...`, old tree `78b2627e...`, old theorem-DAG digest `fb17743f...`,
and the original `[ ]` attempt-zero task row. Worker rules forbid updating it.
`G09-FRESHNESS` is therefore the first failed gate.

The contract also requires the scheduler-owned role map
`.cron/stage1-v2-app-server/role-maps/S56-M-0115-OBLIGATION_TREE.json`.
It is absent, and the worker may not manufacture it. The historical
`obligation-tree-receipt.json` binds the old base and old authority bytes, so
it is retained rather than replaced by a second receipt that could not report
a truthful current passed self-test.

## Bounded Checks

| Command | Exit | Result |
| --- | ---: | --- |
| exact contract-selected validator argv above | 0 | One typed `stale/repair_required` object; `phase_accepted=false`, `phase_predicate_proven=false`, first gate `G09-FRESHNESS`. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 DAG, seven-phase contract, and skill passed before this blocker changed the derived inventory. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 states, two hard edges, five hints, 311 groups, and acyclicity passed before this blocker changed the derived inventory. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0115` | 0 | Rank 23, planned lifecycle, legacy evidence unaccepted, theorem incomplete. |
| resolved `lake env lean --trust=0` scratch replay of `Statement.lean`, then scratch-prefixed replay of `ObligationTree.lean` | 0 | Both elaborated with pinned read-only artifacts; three composers reported the declared standard axiom set. |

No `lake update`, `lake build`, dependency clone/fetch, network use, validator
edit, commit, push, tmux, or nested agent was used. The automation-provided
canonical `.lake` symlink remains a pre-existing untracked path.

Adding this blocker will change the deterministic evidence inventory while the
worker is forbidden to regenerate the checked-in theorem-DAG projection. The
scheduler must reconcile that derived projection during integration; such
inventory reconciliation is not phase acceptance evidence.

## Retry Condition

The scheduler/master lane must publish a refreshed declared obligation-tree
validator and start a fresh claim whose immutable base already contains those
same bytes. It must bind the current theorem DAG, current `[_]` attempt-one
row, current phase artifacts, the scheduler-owned per-item role map, and an
authority-approved phase-scoped ledger solution that preserves the later proof
receipt. Only a schema-exact positive semantic replay can support refreshing
the sole phase receipt and emitting `.stage1-worker-selftest.json`. Master
topology separately requires predecessor acceptance.

This blocker grants no state transition, phase acceptance, proof or provider
credit, `AUDIT-Z`, `THEOREM-Z`, theorem completion, validation, release, or
master acceptance.
