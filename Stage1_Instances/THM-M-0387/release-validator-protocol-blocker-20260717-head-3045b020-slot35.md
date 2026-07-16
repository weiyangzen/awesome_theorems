# THM-M-0387 current-base release blocker

Item: `S56-M-0387-RELEASE`

Intent: `release`

Base revision: `3045b020487392327c4752460c5b048f1cca5331`

Base tree: `a3abeb4373c7513d12024c11ee1a363181f923f9`

Recheck date: `2026-07-17`

## Verdict

`blocked`. This attempt cannot produce the contract-required release receipt or a worker self-test
handoff. The release phase remains `[_]`; this report claims neither release acceptance nor
completion of `AUDIT-Z`, `THEOREM-Z`, or the theorem.

The immediate failure is scheduler-owned validator publication. The release contract selects
exactly one candidate at this worker base:

```text
Stage1_Instances/THM-M-0387/check_release.py
```

Its SHA-256 is
`dbc2a4b7ece983d63968aa0ab87e667483e482ac34428beac574ad38ec5a9c13`, and its
Git blob is `05cd6cdd47b2e7a68053ce78b0e640852bf4eae3`. The exact authority-selected argv,
run from the repository root with no shell interpolation, was:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py
```

It exited `0` with empty stderr and exactly these 100 stdout bytes (including the terminal newline):

```text
release-decision: ok (blocked; validation unaccepted; root M2/open; AUDIT-Z=false; THEOREM-Z=false)
```

The stdout SHA-256 is
`579f2752d394ae9709e54909ed2b3f57df6dca84dc19132e5d9b81cd8e8e0230`; the empty
stderr SHA-256 is
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
This is legacy prose, not the mandatory single JSON object with schema
`stage1-validator-semantic-result/1.0`. Exit zero alone is explicitly insufficient. Because every
validator candidate is scheduler-owned and immutable in worker handoffs, this worker did not create,
edit, rename, replace, or delete a validator. A release receipt cannot truthfully record a compliant
semantic replay, so none is emitted.

## Claim and dependency audit

The exact frontier key is `(1, 6, S56-M-0387-RELEASE)`. The authoritative v2 item is `[_]` with
`attempts=1`; its predecessor `S56-M-0387-VALIDATION` is also `[_]`, not master-accepted `[x]`.
The existing validation receipt uses legacy schema `stage1-worker-validation-receipt/1.0`, binds base
`2e3a5d5130638c6983d4febfd040ca94571e2f68`, reports provisional worker support only, and records
`kernel_closed=false` and `theorem_complete=false`. It therefore cannot satisfy the release
contract's validation-receipt role or the release dependency gate.

The required hard-parent inspection order is exactly `[]`, so it was traversed exactly once with no
parent inspections. There are no direct hard parents, transitive hard ancestors, hard edges, or reuse
hints. All five weak shared-module groups were audited without reuse. Their only inspected member,
`THM-M-0133`, supplies restricted or conditional FLT material rather than an accepted unconditional
root body, and its own seven phases remain `[_]`. No proof body, receipt, checkbox state, or evidence
credit is consumed or inherited.

The current graph SHA-256 is
`6c46a13db8e9d6a299fca9894fba72529f3cd80df81c82e6e4937cbef997f038`; the target
dependency-context SHA-256 is
`90f56448880bb5c1f54b618027daea5b7b32be6e0d05ba2723c43bcc39e17235`.
The tracked `dependency-reuse-ledger.json` predates this claim: it binds graph digest
`6ce46e0d9e79e1a40c423ae1074db34e889702b9a5b5989034cd462615fed604` and repository
revision `7d8182914615a5f5f0445f515fbd635a74bf1faa`. A current-base ledger is required for a
positive phase receipt. It is deliberately not overwritten in this raw blocker handoff: the first
failure occurs before any integrable phase receipt can exist, and changing an established canonical
artifact would not cure the scheduler-owned validator protocol failure. This report records the
fresh closure audit without representing the stale ledger as current evidence.

## Release reconciliation

The truthful terminal facts remain unchanged:

- root vector: `H1 / M2 / R4`;
- minimal mathematical root cut: `M0387-WTW`;
- `audit_complete=false`;
- `theorem_complete=false`;
- accepted receipt IDs: none.

The current release contract additionally requires `release-spec.json`, an authoritative
master-accepted validation receipt, a deterministic evidence bundle, two independent attestations,
public projections derived from that bundle, and `release-receipt.json`. The target has neither
`release-spec.json` nor `release-receipt.json`, and the remaining receipt-bound release artifacts are
not present. The existing `release-decision.json` truthfully says `blocked` with both terminal flags
false, so it is not the contract's accepted or accepted-audit-only terminal decision. These are real
release blockers independently of the validator protocol failure.

## Narrow validation

No `lake update`, `lake build`, dependency clone, dependency fetch, or `.lake` mutation was run. The
automation-provided pinned `.lake` symlink was used read-only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | structural rev-5.6 standard check passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | 7 phases, 12 common gates, and 23 source references passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | v2 graph coverage, ordering, and projections passed |
| `python3 scripts/stage1_target.py check` | 0 | target manifest check passed |
| `python3 scripts/stage1_target.py show THM-M-0387` | 0 | rank 1; planned; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Statement.lean)` | 0 | exact target declaration elaborated |
| `(cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-0387/Proof.lean)` | 1 | pinned cache has no compiled `FltRegular` module; no mutable repair was attempted |
| `python3 Stage1_Instances/THM-M-0387/check_validation.py` | 0 | legacy prose confirms the open M2 root; it is not a typed phase result |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0387/check_release.py` | 0 | legacy prose above; semantic protocol gate failed |

## Retry condition

The scheduler must publish a HEAD-tracked release validator whose unchanged base bytes emit exactly
one conforming `stage1-validator-semantic-result/1.0` JSON object, then allocate a fresh release
claim. A later positive or accepted-audit-only release must also master-accept every predecessor,
bind a current ledger and all contract roles, establish `AUDIT-Z`, and independently resolve or
preserve every mathematical and release-assurance obligation. Until then, there is no phase receipt
and `.stage1-worker-selftest.json` must remain absent.

This is a uniquely named, current-base, target-scoped blocker. It changes no theorem source,
validator, canonical decision, receipt, ledger, blueprint, DAG, checklist, or item state.
