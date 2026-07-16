# THM-M-0387 Intake Validation

## Immutable worker base

- Repository commit: `f545339546bf410d5110d7fe44e70bdcf5d8b48e`
- Repository tree: `6dc924134293b2674df7324ff98b6fdaf660159e`
- V2 blueprint SHA-256: `4d2b5c73fb15ea8ae421329ddfd31778ea10cc58a62800fe46fa7a653a58eea8`
- V2 theorem DAG SHA-256: `39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`
- Dependency context SHA-256: `90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235`
- Phase contract SHA-256: `1e7adf0f4fae0541b3595d4b0bfbb53f7eb17e28a4a889fec14f6df969e0cec4`
- Pinned mathlib commit: `8a178386ffc0f5fef0b77738bb5449d50efeea95`

## Checks

The worker used the existing canonical `.lake` link and did not update, build, fetch, clone, or
otherwise mutate dependencies. The worker ran these structural preflight commands:

```text
python3 Docs/tools/check_stage1_standard.py
python3 Docs/tools/check_stage1_theorem_dag_v2.py
python3 scripts/stage1_target.py check
python3 scripts/stage1_target.py show THM-M-0387
```

All four passed on the current base before the target-owned attempt-4 receipt refresh, as did the
repository-wide validate-only cron projection. After the receipt changes, the two manifest
commands remain green while the two repository DAG checks and validate-only projection truthfully
report one stale reusable-artifact digest: the immutable theorem DAG still binds the prior
`intake-receipt.json` bytes. The worker does not edit either read-only DAG projection or the
authoritative checklist. Integration must merge this owned refresh and regenerate the projections
before master acceptance.

The target validator command is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_intake.py
```

It checks the five intake artifact roles, section-5 planned record, manifest and SSOT identity,
open downstream task DAG, exact dependency-context ledger, complete receipt fields and bindings,
absence of proof credit, and receipt/self-test command agreement. Its only stdout is the required
typed semantic JSON object.

The exact stdout and its SHA-256 are recorded in both the node receipt and worker handoff. It is one
JSON object with the full semantic-result field set required by the HEAD scheduler parser. Actual
independent review and master replay remain integration-owned; local command success is not
represented as master acceptance.

No Lean proof work belongs to intake. The later statement source already exists in this dossier,
but its state and evidence are not used to infer intake acceptance. The pinned Lean environment is
recorded as a downstream input, not as proof of FLT.

## Result boundary

The planned intake predicate is self-tested. The validator may truthfully report
`phase_accepted: true` only for this intake predicate: complete planned dossier, bounded claim,
scope map, source crosswalk, open task DAG, and explicit unresolved boundaries. That semantic field
does not mean master acceptance, accepted exact statement, proof credit, `AUDIT-Z`, or `THEOREM-Z`.

The validator exists at the sole declared candidate path in the worker base and is HEAD-tracked.
This revalidation refreshes the target-owned base/context assertions and provisional receipt without
changing the validator. The integration lane must still bind the selected HEAD artifact roles,
independently review the exact packet, replay the base-identical validator, and issue the master
acceptance receipt. This worker neither infers nor claims those scheduler-owned gates from local
command success.
