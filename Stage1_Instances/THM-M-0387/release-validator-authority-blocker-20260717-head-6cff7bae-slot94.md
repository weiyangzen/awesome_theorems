# THM-M-0387 current-base release authority blocker

Item: `S56-M-0387-RELEASE`

Base revision: `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049`

Base tree: `28c148dbd84fbd549c749f060c92c9a3f00b16d0`

Claim key: `(1, 6, S56-M-0387-RELEASE)`

## Verdict

`blocked`. The release phase is not genuinely self-tested at this base, so this
handoff emits neither `release-receipt.json` nor `.stage1-worker-selftest.json`.
It claims no release acceptance, `AUDIT-Z`, `THEOREM-Z`, theorem completion, or
master acceptance.

The first failed gate is scheduler-owned semantic replay. The HEAD contract
declares three candidate paths and exactly one exists:

```text
Stage1_Instances/THM-M-0387/check_release.py
```

That immutable base file has SHA-256
`dbc2a4b7ece983d63968aa0ab87e667483e482ac34428beac574ad38ec5a9c13`
and Git blob `05cd6cdd47b2e7a68053ce78b0e640852bf4eae3`. The exact selected
argv was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py
```

It exited `0` with empty stderr and exactly 100 stdout bytes:

```text
release-decision: ok (blocked; validation unaccepted; root M2/open; AUDIT-Z=false; THEOREM-Z=false)
```

The stdout SHA-256 is
`579f2752d394ae9709e54909ed2b3f57df6dca84dc19132e5d9b81cd8e8e0230`.
This is legacy prose, not the mandatory single JSON object with schema
`stage1-validator-semantic-result/1.0`. Exit zero alone cannot prove the phase
predicate. The worker did not create, edit, replace, rename, or delete any
validator candidate.

## Dependency And Reuse Audit

The complete hard-parent order is exactly `[]`, so the required traversal was
completed vacuously before release reconciliation. There are no direct hard
parents, transitive hard ancestors, hard edges, or reuse hints.

The five shared-module groups are nonblocking weak co-mentions. Their only other
member, `THM-M-0133`, was inspected through its current phase states, anchor
audit, proof source, validation receipt, and release decision. It supplies only
fixed-exponent or regular-prime bodies and a conditional root composer. Its exact
root remains `M2`, all seven phases remain `[_]`, and it has no accepted
unconditional terminal body. Every shared-group decision therefore remains
`not_applicable`; no body, receipt, checkbox state, or acceptance credit is
consumed or inherited.

The target ledger has schema `stage1-dependency-reuse-ledger/1.1` and the correct
dependency context
`90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235`,
but it binds historical graph and repository revisions. It is not rewritten for
this raw blocker because a ledger-only delta cannot make the immutable validator
protocol pass or support a phase receipt.

## Reconciliation

The truthful release facts remain:

- root vector `H1 / M2 / R4`;
- mathematical root cut `M0387-WTW`;
- `audit_complete=false`;
- `theorem_complete=false`;
- accepted receipt IDs: none.

`S56-M-0387-VALIDATION` is `[_]`, not master-accepted `[x]`. Its receipt is a
historical `stage1-worker-validation-receipt/1.0` packet and reports
`kernel_closed=false` and `theorem_complete=false`. It cannot satisfy the current
release dependency role. The scheduler-owned role map is absent, as are
`release-spec.json`, `release-receipt.json`, a deterministic evidence bundle,
qualifying independent attestations, and public projections generated from an
accepted bundle.

## Narrow Validation

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phase contracts and common gates passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | v2 graph and state projections passed before this blocker was added |
| `python3 scripts/stage1_target.py check` | 0 | target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1, planned, theorem incomplete |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Statement.lean` from `Formalizations/Lean` | 0 | exact statement elaborated |
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Proof.lean` from `Formalizations/Lean` | 1 | pinned cache lacks compiled `FltRegular`; no mutable repair was attempted |
| `python3 Stage1_Instances/THM-M-0387/check_obligation_tree.py` | 0 | 132 obligations, 140 typed edges, root open `M2` |
| `python3 Stage1_Instances/THM-M-0387/check_validation.py` | 0 | legacy narrow handoff confirms the open root; not current acceptance evidence |
| selected release validator argv above | 0 | legacy prose; typed semantic protocol failed |

No `lake update`, `lake build`, dependency clone, dependency fetch, or `.lake`
mutation was performed. The automation-provided pinned `.lake` symlink was used
read-only and remains nonrelease evidence.

## Retry Condition

The scheduler must publish a HEAD-tracked release validator whose unchanged base
bytes emit exactly one conforming typed semantic JSON object, publish the
authority-owned role map, and allocate a fresh release claim. A later terminal
packet must still master-accept every predecessor, bind all required release
roles, establish `AUDIT-Z`, and preserve the open theorem cut unless exact root
closure and every theorem-completion gate independently pass.
