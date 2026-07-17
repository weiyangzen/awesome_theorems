# THM-M-0125 statement validator-authority blocker

## Scope

This is the target-scoped fail-closed result for
`S56-M-0125-STATEMENT` at worker base
`d25efdf450b6236f4750b2eea2cd4f545944d084` (tree
`4674db99ea873d6879a1fa73110c7af3f0884937`). The sole task-state
authority records this item as `[_]` with one attempt and its intake
predecessor as `[_]` with one attempt. This run is therefore a revalidation of
unfinished worker evidence, not a new `[ ] -> [_]` transition and not master
acceptance.

The exact claim tuple is `(v2_execution_rank=278, phase_layer=1,
phase_item_id=S56-M-0125-STATEMENT)`. The authoritative theorem-DAG SHA-256 is
`441c96e3905667f769f2377a70cff6cfd78835d6a92c3862ce6ccbc3bcf505fe`,
and the stable target dependency-context SHA-256 is
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.

## Dependency And Reuse Audit

The supplied `parent_inspection_order`, direct-hard-parent list,
transitive-hard-ancestor list, hard-edge list, reuse-hint list, and shared-group
list are all exactly `[]`. The complete empty sequence was traversed once in
the supplied order before any possible proof work. There were no parent phase
states, receipts, declaration bodies, terminal bodies, or reusable artifacts
to consume. No proof work, exact import, copy, checked transport, checkbox
credit, provider acceptance, or proof credit occurred or transferred. The
empty declared context is not a mathematical-independence claim.

The tracked `dependency-reuse-ledger.json` has the required schema and
truthfully records empty `inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. It is historical provisional evidence:
it binds graph `e8472863...` and repository revision `1cc6aa61...`, not the
current graph and base. It was not refreshed because the immutable validator
pins those bytes and rejects the current base before validating the statement
predicate. A ledger-only edit could not produce a coherent receipt or a
lawful self-test handoff.

## First Failed Gate

`G05-AUTHORITY-REPLAY.validator_semantically_stale_for_current_base` is the
first mechanically unrepairable worker gate. The mandatory HEAD contract
declares these scheduler-owned statement-validator candidates:

- `Stage1_Instances/THM-M-0125/check_statement.py`
- `Stage1_Instances/THM-M-0125/check_statement_artifacts.py`

Exactly the first exists at this worker base. Its SHA-256 is
`ee7b12276f34af731b38b9155c0c119ad0accc0347527533a679ded16b7eef31`,
and its HEAD and worker-base Git blob is
`ea899a7a5d8f22d9d40b5052d1bc181d5110232c`. This worker did not create,
refresh, rename, replace, or delete either candidate.

The exact contract-selected argv was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0125/check_statement.py
```

It exited `1`, wrote no stderr, and emitted exactly one typed JSON object:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"S01-ARTIFACTS","item_id":"S56-M-0125-STATEMENT","message":"negative statement packet validation failed: repository HEAD differs from the claimed worker base","open_obligations":5,"phase":"statement","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0125","verdict":"repair_required"}
```

Standard output is 486 bytes including the final LF, with SHA-256
`d8a3deba0b1b99713874c331e0c32ef81f2595a507937f59eb5e48e4151bd1df`.
The candidate hard-binds base `1cc6aa61...` and tree `dc3053b5...`, while this
claim uses base `d25efdf4...` and tree `4674db99...`. Exit code alone cannot
override the typed `repair_required`, `phase_accepted=false`, and
`phase_predicate_proven=false` result. Worker policy forbids repairing the
declared candidate.

The sole `statement-receipt.json` and schema-1.1 dependency ledger are also
bound to the old base. Replacing them cannot repair the immutable validator
and would violate the exactly-one receipt boundary. There is consequently no
truthful current-base phase receipt and no `.stage1-worker-selftest.json`.

## Independent Statement Blocker

Even after validator maintenance, the positive statement predicate remains
false. The repository supplies only the gloss "elliptic-curve derivative
formula." The source crosswalk identifies at least three materially different
Gross-Zagier results consistent with that gloss:

| Candidate | Source locator | Material boundary |
|---|---|---|
| General Rankin formula | I.(6.3), journal page 230 | weight-two newform, class-group character, Rankin derivative, Heegner divisor, and explicit factors |
| Elliptic application | I.(7.3), journal page 231 | `L'(E,1)` and the height of a rational point up to a real period and rational factor |
| Elliptic base-change identity | V.(2.1), journal page 311 | `L'(E/K,1)`, parametrization, differential norm, traced Heegner point, height, unit index, and discriminant |

No accountable source decision selects and independently reviews one of these
claims or freezes its incorporated definitions, binders, hypotheses,
arithmetic L-series, central point, Heegner object, height and parametrization
conventions, constants, local factors, correction, errata, and degenerate
cases. Selecting whichever form is easiest to encode would broaden, narrow, or
substitute the assigned theorem.

`Statement.lean` therefore remains a two-import boundary probe. With trust
level zero it elaborates `WeierstrassCurve` and `HasDerivAt`, but it declares no
canonical Gross-Zagier proposition. The legacy `S1_M_044.lean` abstract
interface stores caller-supplied derivative, height, normalization, and
hypothesis fields. Neither surface supplies an exact expression, expression or
environment fingerprint, checked transport, mutation result, statement
acceptance, or proof credit.

## Checks Run

All commands ran inside this worker clone. The automation-provided canonical
`.lake` symlink was reused read-only. No `lake update`, `lake build`, dependency
clone/fetch, network operation, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 before owned edit | rev-5.6 structure, target set, v2 DAG, phase contract, and execution skill passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 before owned edit | 1546 theorem nodes, 10822 states, typed relationships, ordering, and acyclicity passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and twenty-three source references passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ordered ranks, and uniform L0/rework-required baseline passed |
| `python3 scripts/stage1_target.py show THM-M-0125` | 0 | rank 44, planned lifecycle, legacy artifacts unaccepted, theorem incomplete |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0125/check_statement.py` | 1 | one typed semantic result reported `failed/repair_required` and `phase_accepted=false`; stderr was empty |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC LEAN_NUM_THREADS=1 lake env lean --trust=0 ../../Stage1_Instances/THM-M-0125/Statement.lean` | 0 | the two generic substrate interfaces elaborated; no exact-target or mutation credit |

Adding this structured blocker changes the generated theorem-DAG evidence
inventory. Post-edit aggregate freshness checks may therefore report expected
projection drift until the master integration lane copies this evidence and
regenerates the read-only projection. Such drift is not phase evidence and
cannot replace the negative semantic replay.

## Retry Condition And Boundary

The scheduler/master lane must commit a refreshed validator at exactly one
declared statement-validator path and issue a fresh claim whose base already
contains those identical bytes. Independently, after intake master acceptance,
an accountable source reviewer must admit one immutable exact primary-source
claim with every theorem-changing convention and boundary fixed. A later
worker can then encode only that approved claim, prove minimal imports, bind
the elaborated expression and environment, compile any credited transports,
execute all four mutation classes, refresh the empty ledger, and replay the
unchanged scheduler validator.

This two-file target-scoped blocker is the only worker-owned delta. It grants
no new state, current phase receipt, self-test handoff, statement acceptance,
proof credit, inherited provider or intake acceptance, `AUDIT-Z`, `THEOREM-Z`,
theorem completion, or master acceptance.
