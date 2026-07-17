# THM-M-0387 current-base release blocker

Item: `S56-M-0387-RELEASE`

Base revision: `c09fec56b723330b06490622768353922c42475f`

Base tree: `0d742d5018bc3b55b0352c28cca02f5d961018fb`

Claim key: `(1, 6, S56-M-0387-RELEASE)`

## Verdict

`blocked`. The release phase is not genuinely self-tested at this base, so this
handoff emits neither `release-receipt.json` nor `.stage1-worker-selftest.json`.
It claims no release acceptance, `AUDIT-Z`, `THEOREM-Z`, theorem completion,
provider acceptance, or state transition.

The first failed gate is scheduler-owned semantic replay. The HEAD release
contract declares three candidates and exactly one exists:

```text
Stage1_Instances/THM-M-0387/check_release.py
```

Its unchanged base SHA-256 is
`dbc2a4b7ece983d63968aa0ab87e667483e482ac34428beac574ad38ec5a9c13`
and its Git blob is `05cd6cdd47b2e7a68053ce78b0e640852bf4eae3`. The
exact required invocation was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py
```

It exited `0` with empty stderr and exactly 100 stdout bytes:

```text
release-decision: ok (blocked; validation unaccepted; root M2/open; AUDIT-Z=false; THEOREM-Z=false)
```

The stdout SHA-256 is
`579f2752d394ae9709e54909ed2b3f57df6dca84dc19132e5d9b81cd8e8e0230`.
This is legacy prose, not the mandatory single
`stage1-validator-semantic-result/1.0` JSON object. Exit zero alone cannot prove
the phase predicate. The worker did not create, edit, replace, rename, or
delete a validator candidate.

## Dependency And Reuse Audit

The complete hard-parent order is exactly `[]`, so it was traversed exactly
once, vacuously, before reconciliation. There are no hard parents, transitive
hard ancestors, hard edges, or reuse hints.

All five weak shared-module groups have only one other member, `THM-M-0133`.
Its authoritative seven phase states are all `[_]`. Its statement, anchor
audit, obligation registry, typed graphs, proof source, validation receipt, and
release decision were inspected at their current bytes. They expose only
definitions, fixed-exponent or regular-prime material, and conditional root
composition. Its exact root remains `M2`, with `AUDIT-Z` and `THEOREM-Z`
unaccepted. Every weak-group decision is therefore `not_applicable`; no proof
body, receipt, checkbox state, or acceptance credit is consumed or inherited.

The target ledger has schema `stage1-dependency-reuse-ledger/1.1` and the exact
context digest
`90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235`,
but it binds historical graph and repository revisions. It is reported as
stale, not represented as current release evidence. Refreshing it cannot cure
the earlier immutable-validator protocol failure or support a release receipt.

## Release Boundary

`S56-M-0387-VALIDATION` is authoritative `[_]`, not master-accepted `[x]`. Its
receipt uses legacy schema `stage1-worker-validation-receipt/1.0`, binds base
`2e3a5d5130638c6983d4febfd040ca94571e2f68`, and records an open `M2` root. It
cannot satisfy the release dependency or current validation-receipt role.

The truthful root vector remains `H1 / M2 / R4`; the mathematical root cut is
`M0387-WTW`; `audit_complete=false`; `theorem_complete=false`; accepted receipt
IDs are empty. The authority-owned role map is absent, as are
`release-spec.json`, `release-receipt.json`, a deterministic evidence bundle,
qualifying independent attestations, and bundle-derived public projections.
Cold/offline, SBOM/license, full trust/TCB, independent-verifier, public
reconciliation, `AUDIT-Z`, `THEOREM-Z`, and master-acceptance gates remain open.

## Narrow Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, v2 DAG, contract, and skill passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phase contracts, 12 common gates, and 23 references passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 phase states, projections, and acyclicity passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 ordered uniform-L0 targets passed |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, theorem incomplete |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Statement.lean` from `Formalizations/Lean` | 0 | exact target elaborated with Lean 4.29.0 |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Proof.lean` from `Formalizations/Lean` | 1 | pinned cache lacks `FltRegular.olean`; no mutable repair attempted |
| `python3 Stage1_Instances/THM-M-0387/check_obligation_tree.py` | 0 | 132 obligations, 140 typed edges, root open `M2` |
| `python3 Stage1_Instances/THM-M-0387/check_validation.py` | 0 | legacy narrow check preserves the open root; not current acceptance evidence |
| selected release validator argv above | 0 | legacy prose; typed semantic protocol failed |

No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was
performed. The automation-provided pinned `.lake` link was used read-only.

After this owned blocker pair was added, the standard and theorem-DAG checks
fail only because the deterministic evidence inventory has not learned the two
new files. Regenerating that read-only projection is master-owned. The blocker
JSON check and diff-hygiene check pass after the handoff.

## Retry Condition

The scheduler must publish a HEAD-tracked release validator whose unchanged
bytes emit exactly one conforming typed semantic JSON object, publish the
authority-owned role map, and allocate a fresh claim. A later release must also
master-accept every predecessor, bind all required release roles, establish
`AUDIT-Z`, and preserve the open theorem cut unless exact root closure and every
theorem-completion gate independently pass.
