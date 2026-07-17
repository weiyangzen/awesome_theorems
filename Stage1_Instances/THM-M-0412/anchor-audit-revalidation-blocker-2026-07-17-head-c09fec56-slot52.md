# THM-M-0412 Anchor-Audit Revalidation Blocker

## Scope

This is the fail-closed worker result for `S56-M-0412-ANCHOR_AUDIT` at
repository base `c09fec56b723330b06490622768353922c42475f` (tree
`0d742d5018bc3b55b0352c28cca02f5d961018fb`) on 2026-07-17 in
`Asia/Shanghai`. The exact claim-order tuple is
`(v2_execution_rank=259, phase_layer=2,
S56-M-0412-ANCHOR_AUDIT)`. The task-state authority records the statement
predecessor and this item as worker-provisional `[_]`, each with one attempt.

The target remains in the closed 1546-item manifest at execution rank 21,
uniform `L0 / rework_required`, planned lifecycle, with legacy artifacts
unaccepted and `theorem_complete=false`.

## First Failed Gate

The first worker-unrepairable gate is
`G05-AUTHORITY-REPLAY.validator_semantic_replay_stale`.

The HEAD anchor contract declares these candidates:

- `Stage1_Instances/THM-M-0412/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0412/check_anchor.py`

Exactly the first exists. It is the scheduler-owned validator already present
at this worker base, with Git blob
`482afc5de18e6b10da52579ae8c30a4eccbb4801` and SHA-256
`c3e639d6ce9c61757d0ba56ae93223493a1cd4bb69a9c2708f4d789be3d810a0`.
This worker did not create, edit, refresh, rename, replace, or delete either
candidate.

The contract-selected argv was run exactly from the repository root:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_anchor_audit.py
```

It exits `1`, writes no stderr, and writes exactly one 463-byte line to stdout
(including its final LF; SHA-256
`a3fa82683a4684765241a51251589a7500b099cca9ec2da2b906067a478809f7`).
That line is one JSON object with schema
`stage1-validator-semantic-result/1.0` and reports:

```json
{"audit_complete":false,"blocked":false,"first_failed_gate":"ANCHOR-AUDIT-SEMANTIC-CHECK","item_id":"S56-M-0412-ANCHOR_AUDIT","message":"repository revision drift","open_obligations":1,"phase":"anchor_audit","phase_accepted":false,"phase_predicate_proven":false,"schema_version":"stage1-validator-semantic-result/1.0","stale_inputs":[],"status":"failed","theorem_complete":false,"theorem_id":"THM-M-0412","verdict":"repair_required"}
```

The immutable validator freezes historical base `307c34d3...`, tree
`ef45ba44...`, theorem-DAG SHA-256 `8be71ef1...`, an earlier ledger digest,
phase state `[ ]`, and attempt count 0. Current HEAD is `c09fec56...`, the
mandatory graph SHA-256 is
`c5d478054cf32914251001d24d128b3b21ba29414965d64947d78768329660bd`,
and the authority now records `[_]` with one attempt. Exit code alone is not
interpreted as acceptance; the typed result expressly has
`phase_accepted=false` and `phase_predicate_proven=false`.

The sole existing `anchor-audit-receipt.json` is also historical. It binds
base `307c34d3...`, records `accepted=false`, and contains stale worker-output
tracking descriptions and an earlier ledger/graph. It is not a current-base
receipt. A worker may not change the protected validator to make a refreshed
receipt pass, so no replacement phase receipt and no
`.stage1-worker-selftest.json` are emitted.

Independently, master topology is open: the statement predecessor is `[_]`,
not accepted `[x]`. This does not alter the earlier first failed worker gate.

## Dependency And Reuse Audit

The current graph and the scheduler-supplied dependency context agree on an
exactly empty closure:

- direct hard parents: `[]`
- transitive hard ancestors: `[]`
- hard edges: `[]`
- reuse hints: `[]`
- shared lemma groups: `[]`
- `parent_inspection_order`: `[]`

The supplied empty order was traversed exactly once before any possible proof
work. No proof work was performed. No provider declaration, terminal proof
body, source bytes, receipt, import, copy, wrapper, checked transport,
checkbox state, acceptance, or evidence credit was consumed or inherited.

The tracked `dependency-reuse-ledger.json` uses schema
`stage1-dependency-reuse-ledger/1.1` and truthfully contains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`. Its current bytes are SHA-256
`146b813c1801dc6e4116a4de040f303c155a3a1cd33b841f613fa026dbd4745a`
(Git blob `a0fd15ad0d923efbfa1ee8af7594a2291aba8876`), but it is owned by the later
obligation-tree packet and binds an earlier base/graph. Overwriting that shared
path for this already-provisional phase would invalidate later target evidence
and still fail the immutable anchor validator's pinned digest. This report
therefore records the discrepancy instead of manufacturing a ledger-only
partial packet. Empty dependency context is not an independent-proof claim.

## Anchor Boundary

The frozen target-owned discovery artifacts remain byte-stable:

- `anchor-audit.json`: SHA-256 `bac3854ea0523b4b7b977e71a2f81924d69a72e353b0cc8fd6f7f9b2e85f919f`
- `discovery-protocol.json`: SHA-256 `94ec324d608a2b477b37667a4e5251ca8d8a81dfed6048e381e15e657843f429`
- `discovery-evidence.json`: SHA-256 `37870224f20aa917a30f6e9312635a4b0ef1bb6898df3963d2b329502fb65f12`
- `AnchorAudit.lean`: SHA-256 `1b499ebc61f5deb9b9ab4cfc869192061333599540b8a9b777d7377dc6042908`

All seven prescribed lanes have bounded results and all six frozen candidates
have an M classification. The source identity and canonical proposition remain
unresolved. The repo-local legacy file is an abstract Nagell-Lutz-shaped
interface, not a concrete terminal theorem. Pinned mathlib supplies adjacent
Weierstrass, discriminant, two-torsion, and affine-point infrastructure; it
indexes the Nagell-Lutz title in `docs/1000.yaml` without `decl` or `decls`.
No immutable external Lean 4 terminal declaration is admitted. Prior
bibliographic evidence distinguishes a 1935 plane-cubic result from a different
1948 Nagell result but does not reconcile either with the catalog's Pierce
label. Selecting one would substitute mathematics.

A current read-only search of every materialized manifest-pinned package found
only `Formalizations/Lean/.lake/packages/mathlib/docs/1000.yaml:2460`, the
declaration-free Nagell-Lutz title row. The target-owned Lean probe elaborates
six adjacent APIs under `--trust=0`, but it supplies no canonical target or
root proof credit.

Accordingly the bounded inventory remains useful guidance, but no candidate
receives H0, M0, M1, checked-transport, proof, phase-acceptance, or theorem
credit. The root remains `H5 / M4 / R4`, discovery saturation is not claimed,
and `audit_complete=false` and `theorem_complete=false`.

## Checks Run

The existing automation-provided `.lake` symlink and pinned mathlib checkout
were used read-only. No `lake update`, `lake build`, dependency clone/fetch, or
cache mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 DAG, acceptance contract, and execution skill passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed context, and acyclicity passed. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and scheduler validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | Rank 21, planned lifecycle, legacy artifacts unaccepted, theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_anchor_audit.py` | 1 | Exactly one typed semantic JSON object; `repair_required`, `phase_predicate_proven=false`, repository revision drift. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0412/AnchorAudit.lean` | 0 | Six pinned adjacent APIs elaborated; no target or proof credit. |
| `rg -n -i 'Pierce conjecture\|Peirce conjecture\|Nagell.Lutz\|Lutz.Nagell\|Trygve Nagell' Formalizations/Lean/.lake/packages` | 0 | Only mathlib's declaration-free Nagell-Lutz title row matched. |
| `git diff --name-only 307c34d3..HEAD -- <target semantic inputs>` | 0 | No catalog, legacy source, statement boundary, crosswalk, manifest, or selected pinned-source input changed. |
| `python3 -m json.tool Stage1_Instances/THM-M-0412/anchor-audit-revalidation-blocker-2026-07-17-head-c09fec56-slot52.json` | 0 | The owned blocker is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0412` | 0 | No whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Handoff correctly absent because the phase predicate is not self-tested. |
| `python3 Docs/tools/check_stage1_standard.py` (post-edit) | 1 | Expected master-integration boundary: the new owned JSON changes generated DAG inventory. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` (post-edit) | 1 | Same expected read-only projection drift; the worker may not regenerate the DAG. |

Adding this owned report changes the deterministic theorem-DAG evidence
inventory. A post-edit aggregate replay may therefore report projection drift
until master integration regenerates the read-only DAG. The worker does not
edit that projection.

## Retry Condition

The scheduler/master authority lane must publish one current, internally
consistent anchor packet: the unique declared validator, anchor-layer empty
ledger, inventory/evidence bindings, validation record, and exactly one
`stage1-node-receipt/1.0` must bind one graph and base. A fresh worker claim
must start from a base already containing that unchanged validator blob. The
statement predecessor must separately reach master-accepted `[x]` before
anchor master closure. A later worker may write the root self-test handoff only
after the unchanged authority argv returns one typed result with
`phase_predicate_proven=true`.

This is current-base, target-scoped blocker evidence only. It does not
self-test or satisfy `S56-M-0412-ANCHOR_AUDIT`, propose a new state, replace
the sole phase receipt or dependency ledger, transfer provider acceptance,
change task state or H/M/R debt, prove the root, claim `AUDIT-Z` or
`THEOREM-Z`, or claim master acceptance.

## Continuation Recheck

A fresh continuation audit found HEAD, task state, candidate selection, and the
typed validator result unchanged. The validator stdout again had SHA-256
`a3fa82683a4684765241a51251589a7500b099cca9ec2da2b906067a478809f7`;
the Lean probe again exited 0; the owned JSON and whitespace checks passed; and
the root self-test remained absent. The same scheduler-owned validator
freshness blocker therefore recurs with no worker-permitted repair.
