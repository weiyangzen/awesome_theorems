# THM-M-1008 release decision handoff

Item: `S56-M-1008-RELEASE`

Base revision: `09a2e94f8f331e8fa7938c55db7dddafb47a6c74`

Decision date: `2026-07-14` (`Asia/Shanghai`)

## Exact verdict

The release verdict is `blocked`. Lifecycle remains `planned`, so no execution vector is accepted.
The intake records `[H1, M3, R3]`, while the later provisional graph and validation receipt record
`[H1, M2, R3]`; the weaker `[H1, M3, R3]` record controls this no-state-change decision. Both
`audit_complete` and `theorem_complete` remain false. No receipt is accepted, and neither `AUDIT-Z`
nor `THEOREM-Z` is claimed.

The first node gate failure is `S56-10.2-DEPENDENCY-ACCEPTANCE`: the prerequisite validation item
is only worker-self-tested `[_]`, its receipt is explicitly `release_grade=false`, and it has no
master acceptance. The first intrinsic release failure is `S56-10.6-HERMETIC-COLD-BUILD`.

## Evidence reconciliation

The exact frozen Hewitt-Savage root locally kernel-elaborates from a placeholder-free proof against
the pinned mathlib closure. The recorded narrow replay reports only `propext`, `Classical.choice`,
and `Quot.sound`. This is useful provisional evidence, not accepted `M0-L`: no structured proof
receipt exists, the proof phase is not master accepted, and the pre-proof graph still has an `M2`
root whose required self-independence route is not the direct probability-idempotence route used by
`Proof.lean`. Under the weaker-status rule, no lifecycle or debt promotion is legal.

`AUDIT-Z` is unavailable because the evidence and debt inventory has not been accepted, the human
source remains `H1`, and readability remains `R3`. Release also lacks complete transitive
provenance/foundation/TCB evidence, an immutable clean empty-cache offline replay, durable
SBOM/license archives, two signed independently provisioned runner attestations, an independently
implemented minimal verifier, a deterministic content-addressed bundle, freshness acceptance, and
master reconciliation. This worker checkout and its shared warm `.lake` symlink are nonrelease
evidence.

## Commands and exact results

Commands ran from the worker clone. No `lake update`, `lake build`, dependency clone/fetch, network
operation, or `.lake` mutation was performed.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups, 1546 uniform-L0 Lean 4 targets

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1008
  exit 0: rank 288, planned, legacy artifacts unaccepted, theorem_complete=false

python3 Stage1_Instances/THM-M-1008/check_release.py
  exit 0:
  PASS THM-M-1008 release reconciliation: validation receipt identity, hashes, and provisional kernel observations agree
  FAIL CLOSED dependency: S56-M-1008-VALIDATION is nonrelease worker evidence and is not master accepted
  FAIL CLOSED authority: planned lifecycle accepts no vector; weaker recorded H1/M3/R3 controls and the direct proof route is not reconciled with the frozen graph
  FAIL CLOSED audit/release: H0, R0, complete trust/provenance, cold offline replay, supply chain, independent verification, and deterministic bundle are absent
  verdict=blocked; lifecycle=planned; audit_complete=false; theorem_complete=false; accepted_receipt_ids=[]

timeout 600s Stage1_Instances/THM-M-1008/check_validation.sh
  exit 0:
  PASS THM-M-1008 network-isolated narrow kernel replay
  PASS exact root/type probe: propext, Classical.choice, Quot.sound
  PASS transitive sorry check: proof root and type probe are sorry-free

python3 -m json.tool Stage1_Instances/THM-M-1008/release-decision.json >/dev/null
  exit 0

git diff --check -- Stage1_Instances/THM-M-1008 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The release checker binds the validation receipt and all reconciled inputs by SHA-256, checks the
manifest and DAG dependency boundary, preserves the stale-graph conflict fail closed, verifies the
full remaining cut set, and validates the worker packet. Retry requires master acceptance and
fresh graph/composition reconciliation, followed by accepted audit, source/readability, trust,
hermetic supply-chain, independent-verifier, deterministic-bundle, freshness, and master release
gates.
