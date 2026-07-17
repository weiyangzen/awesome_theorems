# THM-M-0121 current-base statement blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0121-STATEMENT` at worker base
`d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). It changes no Lean source, prior phase receipt,
dependency ledger, scheduler-owned validator, task-state authority, theorem-DAG projection,
lifecycle, debt vector, or acceptance state.

The sole task-state authority records both `S56-M-0121-INTAKE` and this statement item as `[_]`
with one attempt. Both remain unfinished worker evidence, not master acceptance. The exact claim
tuple is `(v2_execution_rank=274, phase_layer=1,
phase_item_id=S56-M-0121-STATEMENT)`. The current theorem-DAG SHA-256 is
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`, and the stable target
dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency and reuse audit

The authoritative `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group list are all empty.
That exact empty closure was traversed once, before any possible proof work. There were no parent
phase states, receipts, declaration bodies, reusable artifacts, or terminal proof bodies to
inspect. No proof work was performed; no import, copy, or checked transport was used; and no
provider checkbox state, acceptance, or proof credit was transferred.

The tracked `dependency-reuse-ledger.json` has schema
`stage1-dependency-reuse-ledger/1.1` and truthfully records empty `inspections`,
`reuse_decisions`, and `unresolved_compatibility_obligations`. It is historical evidence bound to
repository revision `307c34d30fc3763c82a944a142ae922b48ff18aa` and theorem-DAG digest
`8be71ef1e4fa1c3de5aa420550ff915dbe0b9f165ac0d98518adf2d1fe25fd47`, not current-base evidence.
It is deliberately not refreshed in this blocked run: a ledger-only rewrite cannot repair the
immutable validator or the positive statement predicate and would stale the integrated receipt's
exact input binding. This report binds the current empty closure without presenting that older
ledger as fresh.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_base_binding_stale` is the first mechanically unrepairable worker
gate. The mandatory HEAD phase contract has SHA-256
`1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4` and Git blob
`84b92df9eaf457ab954b652c3f20f4d513cf0a88`. For `statement` it declares these scheduler-owned
candidates:

- `Stage1_Instances/THM-M-0121/check_statement.py`
- `Stage1_Instances/THM-M-0121/check_statement_artifacts.py`

Exactly one exists at the immutable worker base: `check_statement.py`, SHA-256
`c841ab68d902a14de2ba961c98e8ad0a17c9cdbd3e19442587b2dce9d9496e0c`, Git blob
`7ef798a50f2c5b0dbddb63f50a29841ff2baa5e9`. Its worker-tree bytes equal the base blob, so
selection is unambiguous and no validator candidate was created, refreshed, renamed, replaced, or
deleted.

The exact contract-selected command was run without shell interpolation:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0121/check_statement.py
```

It exited `1`. Stdout was exactly one 453-byte JSON object, SHA-256
`b80b5abb48a5e720a15a55d6d5b003bc9f72aab281e0f49e77a4f2eb666ce4dd`:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"VALIDATOR-INTERNAL-CONSISTENCY","item_id":"S56-M-0121-STATEMENT","message":"Validator consistency failure: AssertionError: ","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0121","verdict":"repair_required"}
```

Stderr was the eight-line traceback from the validator's first HEAD assertion, 536 bytes with
SHA-256 `feeb0ac0e2452b6435c7fd2dbe11dcd42785b4a94e14fe87845a7826509eac32`.
The immutable candidate hard-codes repository revision
`307c34d30fc3763c82a944a142ae922b48ff18aa`, tree
`ef45ba442c71959db78ad146a023bcf32946a53f`, obsolete theorem-DAG bytes, and the pre-integration
statement cursor. Current HEAD differs, so the candidate fails before checking its historical
packet. Its typed semantic result is `repair_required` with `phase_accepted=false`; neither exit
status nor an older receipt can override that result. Worker policy forbids repairing the
scheduler-owned candidate, so no current node receipt or worker self-test handoff can be produced.

## Positive statement boundary

Independently, `S02-EXACT-TARGET` and `S03-MUTATIONS` remain open. Repository source evidence gives
only the label "Mori rationality theorem", Mori attribution, a year, and the gloss "rationality of
Fano varieties". It supplies no admitted immutable theorem passage, theorem/page locator,
incorporated definitions, assumptions, corrections, errata disposition, or independently approved
translation. Nef-threshold rationality, rational curves or uniruledness, rational connectedness,
and birational rationality are materially different propositions. The unqualified assertion that
every Fano variety is birationally rational is false in standard meanings. Selecting one reading
would invent, weaken, broaden, or substitute mathematics.

`Statement.lean` therefore remains a declaration-free boundary probe. Its one import,
`Mathlib.AlgebraicGeometry.RationalMap`, exposes three adjacent rational-map interfaces, but it
contains no canonical Mori target, expression or environment fingerprint, checked transport, or
mutation fixture. The tracked statement receipt is correspondingly `accepted=false`,
`verdict=blocked`, with no statement fingerprint and four unexecuted mutation classes. The
provisional intake also leaves the canonical statement and formal target null. No positive phase
predicate, exact statement credit, proof credit, `AUDIT-Z`, or `THEOREM-Z` follows.

## Checks run

All checks ran in this worker clone on 2026-07-17 (Asia/Shanghai). The automation-provided pinned
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, network operation, or package mutation ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, 1546-target manifest, v2 DAG, phase contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed relationships, state preservation, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phase contracts, twelve common gates, and twenty-three source references passed. |
| `python3 scripts/stage1_target.py check` | 0 | The ordered 1546-target `L0/rework_required` manifest passed. |
| `python3 scripts/stage1_target.py show THM-M-0121` | 0 | Rank 40, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| Declared-candidate enumeration and HEAD/base Git-blob comparison | 0 | Exactly one candidate exists, unchanged at this worker base. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0121/check_statement.py` | 1 | Exactly one typed semantic JSON object reported `repair_required`, `phase_accepted=false`, and the stale embedded base. |
| From `Formalizations/Lean`: `LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 /home/sansha-2/.elan/bin/lake env lean --trust=0 ../../Stage1_Instances/THM-M-0121/Statement.lean` | 0 | The three adjacent rational-map interfaces elaborated; no canonical target or proof body was declared. |

The structural and Lean checks are bounded observations. They cannot replace the failed mandatory
semantic replay or satisfy the exact-statement predicate.

## Retry condition and status boundary

The scheduler/master lane must publish a current-authority validator at exactly one declared path
and issue a fresh claim whose immutable worker base already contains that unchanged blob. Source
authority must separately admit and independently approve one exact immutable theorem passage and
freeze every incorporated definition, domain, ordered binder, hypothesis, conclusion, correction,
erratum, and boundary case. A fresh statement worker can then refresh the empty schema-1.1 ledger,
encode only that approved claim, minimize pinned imports, fingerprint the expression and
environment, compile all credited transports, execute all four required mutation classes, emit
exactly one current receipt, and replay the unchanged validator.

This artifact is a target-scoped scheduler/source-identity blocker only. It grants no state
transition, phase acceptance, accepted receipt, provider acceptance transfer, exact-statement or
proof credit, audit completion, theorem completion, or master acceptance. Because the assigned
phase is not genuinely self-tested at this base, `.stage1-worker-selftest.json` is intentionally
absent.
