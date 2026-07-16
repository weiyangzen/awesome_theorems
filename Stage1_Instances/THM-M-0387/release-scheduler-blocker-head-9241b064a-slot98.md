# THM-M-0387 current-base release blocker

Item: `S56-M-0387-RELEASE`

Claim key: `(1, 6, S56-M-0387-RELEASE)`

Base: `9241b064a32cea3e16eb45d156fef8a2577704b0` / tree
`c60b403a3058af0bbf32405a99c931274675784a`

## Verdict

`blocked`. No contract-compliant release receipt or worker self-test handoff can be emitted from
this base. The authoritative item and its validation predecessor are both `[_]`. The lifecycle
remains `planned`, the root remains `H1/M2/R4`, and both `audit_complete` and
`theorem_complete` remain false.

The immediate failure is scheduler-owned validator publication. The release contract selects
exactly one candidate, `Stage1_Instances/THM-M-0387/check_release.py`, at SHA-256
`dbc2a4b7ece983d63968aa0ab87e667483e482ac34428beac574ad38ec5a9c13` and Git blob
`05cd6cdd47b2e7a68053ce78b0e640852bf4eae3`. The authority-selected command was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py
```

It exited zero with empty stderr and 100 stdout bytes:

```text
release-decision: ok (blocked; validation unaccepted; root M2/open; AUDIT-Z=false; THEOREM-Z=false)
```

That stdout has SHA-256
`579f2752d394ae9709e54909ed2b3f57df6dca84dc19132e5d9b81cd8e8e0230`, but it is prose,
not the required single `stage1-validator-semantic-result/1.0` JSON object. Exit zero alone is
insufficient. The worker did not edit, replace, add, rename, or delete any validator candidate.

## Dependency And Reuse Audit

The exact `parent_inspection_order` is `[]`; it was traversed once. There are no direct hard
parents, transitive hard ancestors, hard edges, or reuse hints. The five weak shared-module groups
were rechecked through their only other member, `THM-M-0133`. That dossier contains only the FLT
definition, restricted exponent or regular-prime bodies, a conditional composer, and a gapped
external root candidate. None is an accepted unconditional FLT root body. No declaration, receipt,
checkbox state, or acceptance credit is reused.

The current theorem DAG SHA-256 is
`b0d43b142ed4d47aba3b66062c8303e96a736f259e50ef764918040521449c3a`; the stable context
digest is `90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235`. The tracked
dependency ledger is stale: it binds graph
`6ce46e0d9e79e1a40c423ae1074db34e889702b9a5b5989034cd462615fed604` and revision
`7d8182914615a5f5f0445f515fbd635a74bf1faa`. It is reported as stale rather than overwritten
or presented as current evidence because the scheduler-owned validator failure prevents a lawful
phase receipt.

## Release Boundary

The validation receipt is legacy schema `stage1-worker-validation-receipt/1.0`, binds revision
`2e3a5d5130638c6983d4febfd040ca94571e2f68`, and has no master acceptance. It cannot satisfy
the release dependency or the current `validation_receipt` role.

The minimal mathematical cut remains `M0387-WTW`. Accepted H0/R0, complete trust and TCB closure,
immutable clean cold/offline replay, SBOM/licenses, deterministic release bundle, two qualifying
independent attestations, an independent minimal verifier, and bundle-derived public projections
are also absent. The required `release-spec.json`, `release-receipt.json`, and scheduler-owned role
map do not exist. Therefore neither an accepted theorem release nor `accepted_audit_only` is
available: `AUDIT-Z` itself is still open.

## Narrow Checks

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure and all 1546 targets passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, 23 references passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | v2 graph and projections passed |
| `python3 scripts/stage1_target.py check` | 0 | target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Statement.lean)` | 0 | exact target elaborated with Lean 4.29.0 |
| `(cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Proof.lean)` | 1 | pinned cache lacks compiled `FltRegular`; no mutable repair attempted |
| `python3 Stage1_Instances/THM-M-0387/check_validation.py` | 0 | legacy check preserved open M2 classification only |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py` | 0 | legacy prose; semantic protocol failed |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

## Retry Condition

The scheduler must first publish a HEAD-tracked release validator whose unchanged base bytes emit
one exact typed semantic result, then allocate a fresh release claim. A later accepted or
accepted-audit-only release must additionally bind a current ledger and all authority-selected
roles, depend on master-accepted validation, establish `AUDIT-Z`, and preserve every open theorem
and release obligation truthfully.

This blocker is the only current attempt artifact. There is no `release-receipt.json` and no
`.stage1-worker-selftest.json`; it claims no phase acceptance or theorem completion.
