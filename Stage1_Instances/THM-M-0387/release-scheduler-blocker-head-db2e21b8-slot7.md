# THM-M-0387 current-base release blocker

Item: `S56-M-0387-RELEASE`

Base: `db2e21b8fec263c5b65014acb1ee2039566e35a3`

Claim key: `(1, 6, S56-M-0387-RELEASE)`

## Verdict

`blocked`. This current-base attempt cannot lawfully emit `release-receipt.json` or the root
`.stage1-worker-selftest.json`. It claims no release acceptance, `AUDIT-Z`, `THEOREM-Z`, theorem
completion, inherited proof credit, or task-state transition.

The release contract selects exactly one HEAD-tracked validator candidate,
`Stage1_Instances/THM-M-0387/check_release.py`. Its SHA-256 is
`dbc2a4b7ece983d63968aa0ab87e667483e482ac34428beac574ad38ec5a9c13` and its Git blob is
`05cd6cdd47b2e7a68053ce78b0e640852bf4eae3`. The exact scheduler-owned invocation was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py
```

It exited zero with empty stderr, but stdout was 100 bytes of legacy prose:

```text
release-decision: ok (blocked; validation unaccepted; root M2/open; AUDIT-Z=false; THEOREM-Z=false)
```

The stdout SHA-256 is
`579f2752d394ae9709e54909ed2b3f57df6dca84dc19132e5d9b81cd8e8e0230`; the empty stderr
SHA-256 is `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
This is not the required single JSON object with schema
`stage1-validator-semantic-result/1.0`. Exit zero alone is insufficient, and workers may not edit,
replace, rename, create, or delete validator candidates. Therefore no contract-compliant phase
receipt can be produced on this base.

## Dependency and reuse audit

The authoritative item and its validation predecessor are both `[_]`; the predecessor is not
master-accepted `[x]`. Its receipt is legacy `stage1-worker-validation-receipt/1.0`, binds revision
`2e3a5d5130638c6983d4febfd040ca94571e2f68`, and records `kernel_closed=false` and
`theorem_complete=false`. It cannot satisfy the current release dependency or validation-receipt
role.

The required hard-parent inspection order is exactly `[]`, traversed once. There are no direct hard
parents, transitive hard ancestors, hard edges, or reuse hints. All five weak shared-module groups
were re-audited against `THM-M-0133`; they contain only the FLT definition, exponent-three or
exponent-four branches, regular-prime material, conditional composition, or a gapped external root
candidate. Nothing is reused, and no provider checkbox, receipt, body, or acceptance credit is
inherited.

The current graph SHA-256 is
`91ea782c662e40b9608f8900ad586114c5ef8e8e5d2d2f13316185bd8f205067`; the dependency context is
`90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235`. The tracked ledger binds
older graph `39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c` and revision
`f545339546bf410d5110d7fe44e70bdcf5d8b48e`. It is reported as stale, not presented as current
evidence. Refreshing it would not cure the earlier scheduler-owned validator protocol failure.

## Release boundary

The root vector remains `H1/M2/R4`. `M0387-WTW` is the minimal mathematical root cut, and neither
`audit_complete` nor `theorem_complete` is true. Required H0/R0 review, root trust and TCB closure,
immutable clean cold/offline reproduction, SBOM/licenses, deterministic bundle, two independent
attestations, independent minimal verifier, bundle-derived public projections, `release-spec.json`,
`release-receipt.json`, and the scheduler-owned role map are absent.

The structural standard, phase-contract, theorem-DAG, target-manifest, exact statement, legacy
validation-boundary, and legacy release-consistency checks passed. `Proof.lean` failed narrowly
because the pinned read-only cache lacks `FltRegular.olean`; no `lake update`, `lake build`, fetch,
clone, or `.lake` mutation was attempted.

Those structural and theorem-DAG checks passed at the worker base. After this target-owned blocker
was added, they fail only because the generated theorem-DAG evidence inventory has not yet learned
the new file. Regenerating that read-only projection is master-owned, so this worker did not edit it.
The phase-contract check, blocker JSON check, and diff-hygiene check still pass after the handoff.

## Retry condition

The scheduler must publish a typed semantic release validator unchanged at a future worker base and
allocate a fresh claim. A later positive or audit-only release must additionally bind a current
ledger and every authority-selected role, depend on master-accepted validation, establish
`AUDIT-Z`, and preserve all open mathematical and release-assurance obligations truthfully.
