# THM-M-0412 anchor-audit revalidation blocker

## Scope

This is the fail-closed current-base result for `S56-M-0412-ANCHOR_AUDIT` at
worker base `6cff7bae0e4547cf9ad8b7abaae20d1abb9fe049` (tree
`28c148dbd84fbd549c749f060c92c9a3f00b16d0`). The exact claim order is
`(v2_execution_rank=259, phase_layer=2,
S56-M-0412-ANCHOR_AUDIT)`. This report changes no theorem source, prior phase
receipt, scheduler-owned validator, task-state authority, theorem-DAG
projection, lifecycle, debt vector, or acceptance state.

## First Failed Gate

`G05-AUTHORITY-REPLAY.validator_semantic_replay_stale` is the first
mechanically unrepairable worker gate. The HEAD anchor-audit contract declares
two candidate paths, and exactly one exists:

- `Stage1_Instances/THM-M-0412/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0412/check_anchor.py` (absent)

The selected validator is tracked at this worker base and HEAD with unchanged
Git blob `482afc5de18e6b10da52579ae8c30a4eccbb4801` and SHA-256
`c3e639d6ce9c61757d0ba56ae93223493a1cd4bb69a9c2708f4d789be3d810a0`.
The scheduler-owned selection recipe has SHA-256
`fa75e792ea430af3d54f136809b8baa43610d6b352b59ee5681d2de0b8299463`
and requires this exact argv:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_anchor_audit.py
```

That replay exits `1` and emits exactly one JSON object with schema
`stage1-validator-semantic-result/1.0`. It reports `status=failed`,
`verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, `audit_complete=false`,
`theorem_complete=false`, and `message="repository revision drift"`.

The validator, inventory, and existing receipt are frozen to historical worker
base `307c34d3...` and theorem-DAG SHA-256 `8be71ef1...`. The current base is
`6cff7bae...`, and the mandatory graph SHA-256 is `80cf0510...`. The protected
validator would also reject the current graph and `[_]` phase state if its first
revision check were bypassed. The worker is forbidden to refresh, replace,
rename, or add a declared validator candidate. Exit-zero structural or Lean
checks cannot substitute for this typed negative semantic result.

The tracked `anchor-audit-receipt.json` is likewise historical evidence. It
binds base `307c34d3...`, records `accepted=false`, and cannot serve as the
exactly one current-base phase receipt. This run therefore emits no replacement
phase receipt and no `.stage1-worker-selftest.json`.

Independently, `G02-TOPOLOGY` is not ready for master closure: the statement
predecessor and this anchor-audit item are authoritative `[_]`, not
master-accepted `[x]`.

## Dependency And Reuse Audit

The complete supplied `parent_inspection_order`, direct-parent list,
transitive-ancestor list, hard-edge list, reuse-hint list, and shared-group list
are all empty. The exact empty parent order was traversed once before any
possible proof work. No proof work was performed. No provider declaration,
terminal proof body, receipt, import, copy, checked transport, checkbox state,
acceptance, or evidence credit was consumed or inherited.

The tracked schema-1.1 `dependency-reuse-ledger.json` truthfully retains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, but it is now owned by the later
`S56-M-0412-OBLIGATION_TREE` packet and binds graph `d5b27da9...` and repository
revision `a103f2e1...`, not this anchor revalidation claim. A ledger-only rewrite
cannot make the protected validator pass or support a current receipt, so this
blocked run records the stale binding without manufacturing a partial self-test
packet. Empty dependency context is not a mathematical-independence claim.

## Anchor Boundary

The frozen six-candidate, seven-lane inventory remains useful guidance. A
current read-only repository and manifest-pinned package search found no changed
target semantic input and no new terminal candidate. Across every materialized
package, the only exact-topic match remains mathlib's
`docs/1000.yaml:2460` title row for the Nagell-Lutz theorem; that row has no
`decl` or `decls`. The target-owned `AnchorAudit.lean` probe still elaborates
six adjacent Weierstrass and affine-point APIs under `--trust=0`, but they are
support infrastructure only.

The repo-local legacy module remains an abstract Nagell-Lutz-shaped interface
that assumes proposition-valued branch data and supplies no concrete catalog
theorem or terminal proof body. Prior content-bound bibliographic evidence still
distinguishes a 1935 plane-cubic result from a different 1948 Nagell result and
does not reconcile either with the catalog's Pierce label. No concrete immutable
external Lean 4 project, module, declaration, or source body is admitted.

Accordingly, the source identity and canonical proposition remain unresolved;
the root remains `H5/M4/R4`; and no candidate receives H0, M0, M1, checked
transport, proof, or acceptance credit. These are bounded observations, not
global search saturation. `audit_complete=false` and
`theorem_complete=false`.

## Checks Run

All commands ran from this worker clone. The canonical automation-provided
`.lake` link was reused read-only; no Lake update/build, dependency clone/fetch,
or cache mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure, theorem DAG, contract, and target surface passed before this report was added. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed context, and acyclicity passed before this report was added. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and scheduler validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered L0/rework-required targets passed. |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | Rank 21, planned target, legacy artifacts unaccepted, theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0412/check_anchor_audit.py` | 1 | Exactly one typed semantic object; `repair_required`, message `repository revision drift`. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0412/AnchorAudit.lean` | 0 | Six pinned adjacent APIs elaborated; no target or proof credit. |
| bounded `rg` over every materialized manifest-pinned package | 0 | Only mathlib's declaration-free Nagell-Lutz title row matched the exact-topic family. |

Adding this new target-owned report changes the deterministic theorem-DAG
evidence inventory. A final aggregate replay may therefore report expected
projection drift until the master integration lane copies the report and
regenerates the read-only DAG. That is not phase evidence and cannot replace the
negative semantic validator result.

## Retry Condition

The scheduler/master lane must refresh the sole declared validator and the
target-owned dependency ledger, inventory bindings, and exactly one phase
receipt against one current graph/base, then commit them before issuing a fresh
claim whose base contains the unchanged validator blob. The statement
predecessor must be separately master-accepted `[x]` before anchor-audit master
closure. A fresh worker may write the self-test handoff only after the unchanged
exact argv returns one typed result with `phase_predicate_proven=true`.

This is current-base, target-scoped revalidation blocker evidence only. It does
not self-test or accept `S56-M-0412-ANCHOR_AUDIT`, replace its historical
receipt, refresh the ledger, change task state, transfer provider acceptance,
prove the root, claim `AUDIT-Z` or `THEOREM-Z`, or claim master acceptance.
