# THM-M-0387 Intake Validation

## Immutable worker base

- Repository commit: `c5037228977a81948bbd6119e1728b4b65b9924e`
- Repository tree: `78b2627e717156dffe240bea12d14205af667d2a`
- V2 theorem DAG SHA-256: `fb17743ff737fd3c528467b6f992a7235a36f0842b528e57de3e4c6d660d3518`
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

All four passed during preflight before the new target-owned JSON files were created. The receipt
and worker packet record the final post-edit results, not those earlier successes. After creation, the
manifest/target checks still pass, while the standard and v2 graph checks intentionally report
that the checked-in theorem DAG differs from fresh generation: its derived evidence inventory now
sees `intake-receipt.json` and `task-dag.json`. The worker is forbidden to edit that read-only
projection. The integration transaction merges the owned files, regenerates the theorem DAG, and
reruns both validators. This expected projection drift is recorded as a known handoff boundary
rather than hidden as a passing final result.

The target validator command is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_intake.py
```

It checks the five intake artifact roles, section-5 planned record, manifest and SSOT identity,
open downstream task DAG, exact dependency-context ledger, complete receipt fields and bindings,
absence of proof credit, and receipt/self-test command agreement. Its only stdout is the required
typed semantic JSON object.

The scheduler acceptance unit suite was also run. Twenty-seven tests passed and three replay
environment tests failed before semantic review: this managed worker cannot write a probe secret
under the read-only home directory, and `/usr/bin/bwrap` fails the suite's root-ownership/permission
precondition. The target validator stdout was independently fed to the scheduler's exact semantic
parser and accepted as one schema-valid object. Actual master replay remains integration-owned and
fail-closed; the environment failures are not represented as positive replay evidence.

No Lean proof work belongs to intake. The later statement source already exists in this dossier,
but its state and evidence are not used to infer intake acceptance. The pinned Lean environment is
recorded as a downstream input, not as proof of FLT.

## Result boundary

The planned intake predicate is self-tested. The validator may truthfully report
`phase_accepted: true` only for this intake predicate: complete planned dossier, bounded claim,
scope map, source crosswalk, open task DAG, and explicit unresolved boundaries. That semantic field
does not mean master acceptance, accepted exact statement, proof credit, `AUDIT-Z`, or `THEOREM-Z`.

The validator was absent from the historical worker base and is new in this revalidation handoff.
The HEAD contract also requires the integration lane to select a validator whose HEAD blob equals
the worker-base blob. Therefore master replay remains fail-closed until the integration lane first
lands these owned bytes and performs a fresh review/replay against a base containing the validator.
This worker neither infers nor claims that scheduler-owned gate from local command success.
