# THM-M-0130 statement revalidation: scheduler-owned validator is stale

Item: `S56-M-0130-STATEMENT`

Worker base: `c6ccce54afcb261a3b4c236a3eb538a1e4b829a8` (tree
`13ac09d107589b9b20956e6d2e4c0696058a0b41`).

## Decision

This assigned statement phase is not current-base self-tested. The sole HEAD-declared statement
validator exists at the worker base and was not modified, but it hard-pins historical worker base
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`, tree
`daabee9f9b2c6e98d84b6290f78a209b950485fc`, theorem-DAG SHA-256
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153`, and the earlier execution
skill bytes. The mandatory current-base replay exits 1 and emits a semantic
`repair_required` result before proving the phase predicate. The worker contract forbids refreshing,
replacing, renaming, or deleting this scheduler-owned candidate, so no new receipt or worker
self-test handoff can truthfully be issued.

The independent mathematical blocker also remains. The catalog supplies the topic `志村簇` and the
phrase `Hodge型志田簇的构造`, not one truth-valued proposition with an immutable primary-source
locator, definitions, ordered binders, hypotheses, conclusion, model, base, level, prime
restrictions, or boundary cases. The analytic quotient, canonical model over the reflex field, and
Hodge-type integral model are materially different claims. Selecting one for ease of encoding would
broaden or substitute the received mathematics. The exact-target and four mutation gates therefore
remain open even after validator maintenance.

## Claim Order And Dependency Audit

The sole task-state authority records this item as worker-provisional `[_]`, attempt 1, after the
also-provisional intake item. The claim order is exactly `(263, 1,
S56-M-0130-STATEMENT)`. The assigned theorem-DAG SHA-256 is
`95128825a99c9863fc09b6edc8a4a99ab5fae8e0927e40af88635f8945d2aa3e`; the stable dependency-context
SHA-256 is `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

The complete required parent inspection order is `[]`. It was traversed exactly once as that empty
sequence before Lean replay. There are no direct hard parents, transitive hard ancestors, hard
edges, reuse hints, or shared lemma groups. No provider source, declaration, receipt, checkbox state,
acceptance, or proof credit was consumed or transferred.

The tracked schema-1.1 ledger correctly describes the same empty closure, but it is stale for this
claim: it binds repository revision `94009a6b...` and graph SHA-256 `eaee68bd...`. Refreshing it alone
would invalidate both the immutable validator's pinned bytes and the historical phase receipt. This
report records the current empty-closure audit without manufacturing a coherent phase packet.

## Contract And Artifact Audit

HEAD contract SHA-256 is
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`. It declares two candidates:

- `Stage1_Instances/THM-M-0130/check_statement.py`
- `Stage1_Instances/THM-M-0130/check_statement_artifacts.py`

Exactly the first exists and is tracked at HEAD, with SHA-256
`f5d08ee514d8f7eddb0c904af2fe2c471471045c23bd361afda0583f08496dd1` and Git blob
`b17dc0d4c5949b239cffc796da28389808768d1e`. It is the unique scheduler-selected validator and is
immutable to this worker.

The contract resolves exactly one tracked file for each statement role:

| Role | Path | SHA-256 | Git blob |
|---|---|---|---|
| statement record | `Stage1_Instances/THM-M-0130/statement.json` | `5f73036920551ab9eaf5e8bb734c76f72e0c286a4aa5ee744cda5834f380f0e0` | `9277276bcec460062c59d010de0db95be0a397ad` |
| statement source | `Stage1_Instances/THM-M-0130/Statement.lean` | `72d5a1040326613d7a34912ac02325715f3d8345500386cc60eec74065249871` | `acd453b162db97d5661a5ffd00a789f5e4ea7284` |
| source crosswalk | `Stage1_Instances/THM-M-0130/source_statement_crosswalk.md` | `c96ba5a25645fc927efd4e49b90f315052e060ca3413cb7ee2a69edc9652c585` | `451cd64cdad8ccc1f9bb2566592fb95ebb9c5399` |
| phase receipt | `Stage1_Instances/THM-M-0130/statement-receipt.json` | `2cd9637bb14f58bd88190f388c93f6e847c3060d568dc665caf5b36cdfaf488e` | `ecfd9a2fb70b8024344046a4598ed6b466d20793` |

The selected receipt is historical, has `accepted=false`, `verdict=blocked`, and binds base
`94009a6b...`; it is not current-base evidence. Exactly one phase receipt already exists, so this
worker does not create a second receipt or rewrite the historical one without a successful immutable
validator replay.

## Validation

Pre-artifact structural checks passed:

- `python3 Docs/tools/check_stage1_standard.py`: exit 0; 15 assurance groups and all 1546 targets.
- `python3 Docs/tools/check_stage1_theorem_dag_v2.py`: exit 0; 1546 theorem nodes, 10822 states,
  2 hard edges, 5 reuse hints, 311 shared groups, and acyclicity.
- `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py`: exit 0; 7 phases, 12 common gates,
  and 23 source references.
- `python3 scripts/stage1_target.py check`: exit 0; 1546 unique uniform-L0 targets.
- `python3 scripts/stage1_target.py show THM-M-0130`: exit 0; rank 26, planned, legacy evidence
  unaccepted, theorem incomplete.

The mandatory validator command was exactly:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0130/check_statement.py
```

It exited 1. Stderr reported `ValueError: repository HEAD differs from the worker base`. Stdout was
exactly one JSON object with schema `stage1-validator-semantic-result/1.0`, item and theorem identity,
`status=failed`, `verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, `audit_complete=false`, `theorem_complete=false`, and
`first_failed_gate=VALIDATOR-INTERNAL-CONSISTENCY`. Stdout was 499 bytes including its final LF with
SHA-256 `cc362ace9f02b5bdd51736a20ae3931b6d0f95341e5543a46961621ad00bb443`; stderr was 753 bytes with
SHA-256 `1c7acb47e2eabde9db401049701cc8756fb7533b1b907293f33f63d035afbb19`. Exit success was not inferred,
and the typed negative result cannot support master acceptance.

The narrow pinned Lean replay

```text
cd Formalizations/Lean && LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 \
  lake env lean --trust=0 ../../Stage1_Instances/THM-M-0130/Statement.lean
```

exited 0 and printed `Scheme : Type (u + 1)` plus three sandbox stream-fd warnings. It validates only
the declaration-free scheme boundary, not an exact Shimura-variety target. The legacy
`AwesomeTheorems/Stage1/S1_M_026.lean` also elaborated and exposed its local-skeleton/open-closure
markers. A bounded pinned-tree search for `Shimura`, `reflex field`, or `Hodge type` returned the
expected no-match result. No prohibited Lean proof escape matched the target statement or legacy
module.

The existing automation `.lake` symlink was used read-only. Lean is 4.29.0, mathlib is pinned at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` with tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`, and the mathlib worktree is clean. No update, build,
clone, fetch, or dependency mutation was performed.

## Retry And Status Boundary

The scheduler/master authority must land a coherent refreshed declared validator, current-graph
schema-1.1 ledger, and sole current-base phase receipt, then issue a fresh claim containing the
unchanged validator blob. Separately, intake must be master accepted and an accountable source owner
must preserve and approve one immutable primary-source theorem or construction passage, freezing
every incorporated definition, assumption, correction, binder, conclusion, and boundary case.
Only then can the exact target be encoded, imports minimized, expression and environment
fingerprints bound, transports checked, and all four mutation classes run.

This is current-base target-scoped blocker evidence only. It does not re-propose or satisfy the
already-provisional statement phase, alter task state, refresh the ledger or receipt, accept a
statement, transfer proof credit, or claim `AUDIT-Z`, `THEOREM-Z`, theorem completion, or master
acceptance. Because the mandatory validator failed semantically, `.stage1-worker-selftest.json` is
intentionally absent.
