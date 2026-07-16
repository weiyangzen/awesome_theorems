# THM-M-0134 anchor-audit revalidation blocker

## Scope

This is the fail-closed current-base result for `S56-M-0134-ANCHOR_AUDIT` at
worker base `f545339546bf410d5110d7fe44e70bdcf5d8b48e` (tree
`6dc924134293b2674df7324ff98b6fdaf660159e`). The authoritative claim tuple is
`(v2_execution_rank=284, phase_layer=2,
S56-M-0134-ANCHOR_AUDIT)`. This report changes no theorem source, prior phase
receipt, validator, task-state authority, theorem-DAG projection, lifecycle,
debt vector, or acceptance state.

## First Failed Gate

`G05-AUTHORITY-REPLAY.validator_semantic_replay_stale` is the first
mechanically unrepairable worker gate. The HEAD anchor-audit contract declares
two candidate paths, and exactly one exists:

- `Stage1_Instances/THM-M-0134/check_anchor_audit.py`
- `Stage1_Instances/THM-M-0134/check_anchor.py` (absent)

The selected Python validator is tracked at both the worker base and HEAD with
unchanged Git blob `e0bbc3c9afd841322ed488637cad2bb406c58f1c` and SHA-256
`f53625b4690d1fc6fd88ac6ac945516b0bfce07f936dd8e916e8792c2748f40d`.
Its exact contract argv is:

```text
/usr/bin/python3 -I -B Stage1_Instances/THM-M-0134/check_anchor_audit.py
```

That replay exits `1` and emits exactly one JSON object with schema
`stage1-validator-semantic-result/1.0`. It reports `status=failed`,
`verdict=repair_required`, `phase_accepted=false`,
`phase_predicate_proven=false`, `audit_complete=false`,
`theorem_complete=false`, and `message="theorem DAG digest drift"`.

The validator is frozen to worker base `778c2db4...` and theorem-DAG SHA-256
`9db2a7cc...`. The current base is `f5453395...`, and the current authoritative
theorem-DAG SHA-256 is
`39dc7ce5f668c527de899e74c99840aef50e6be4c576aaf146abed1b6749275c`.
The worker is forbidden to refresh, replace, rename, or add a declared
validator candidate. Exit-zero structural or Lean checks cannot substitute for
the typed negative semantic result.

The tracked `anchor-audit-receipt.json` is also historical evidence: receipt
`S56-M-0134-ANCHOR-AUDIT-WORKER-20260717-V1` binds base `778c2db4...`, has
`accepted=false`, and cannot serve as the exactly one current-base phase
receipt. This run therefore emits no replacement phase receipt and no
`.stage1-worker-selftest.json`.

Independently, `G02-TOPOLOGY` is not ready for master closure. The statement
predecessor and this anchor-audit item are authoritative `[_]`, not
master-accepted `[x]`.

## Dependency And Reuse Audit

The complete supplied `parent_inspection_order`, direct-parent list,
transitive-ancestor list, hard-edge list, reuse-hint list, and shared-group list
are all empty. The exact empty closure was traversed once before any possible
proof work. No proof work was performed. No provider phase state, receipt,
declaration, terminal proof body, import, copy, checked transport, checkbox
state, acceptance, or evidence credit was consumed or inherited.

The current schema-1.1 `dependency-reuse-ledger.json` truthfully contains empty
`inspections`, `reuse_decisions`, and
`unresolved_compatibility_obligations`, and it binds the stable dependency
context
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
It remains bound to graph `9db2a7cc...` and repository revision `778c2db4...`,
not this claim. A ledger-only refresh cannot make the protected validator pass
or support a current receipt, so this blocked run records the stale binding
without manufacturing a partial self-test packet. The empty context is an
audited absence of graph relationships, not a mathematical-independence or
proof claim.

## Anchor Boundary

The tracked bounded inventory remains useful guidance. It has six classified
candidates across the seven prescribed ordered lanes. The repo-local legacy
module supplies a checked statement shape and conditional
`BurnsideYoungProofPackage` wrappers, but no package inhabitant or terminal
classification proof. Pinned mathlib at immutable revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` supplies partitions, Young diagrams,
semistandard tableaux, finite permutation groups, bundled representations, and
irreducibility substrate, but no located Specht-module construction or exact
symmetric-group irreducible-classification theorem.

A fresh bounded read-only search found no new exact-topic Lean declaration in
the pinned package closure. No concrete immutable external Lean 4 terminal
candidate or admitted primary passage is available. These are bounded
observations, not global saturation. The canonical statement remains null, the
root remains `H4/M4/R4`, and no candidate receives proof credit. Thus
`audit_complete=false` and `theorem_complete=false`.

## Checks Run

All commands ran from this worker clone. The canonical `.lake` link was used
read-only; no Lake update/build, dependency clone/fetch, or cache mutation was
performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Rev-5.6 structure and the 1546-target uniform-L0 surface passed. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorem nodes, 10822 phase states, typed context, and acyclicity passed before this blocker was added. |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | Seven phases, twelve common gates, and scheduler validator rules passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets and ranks passed. |
| `python3 scripts/stage1_target.py show THM-M-0134` | 0 | Rank 50, planned L0/rework-required target, legacy artifacts unaccepted, theorem incomplete. |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0134/check_anchor_audit.py` | 1 | Exactly one typed semantic JSON object; `repair_required`, message `theorem DAG digest drift`. |
| bounded exact-topic `rg` over the repository and pinned Lean packages | 0 for repository hits only | The only material exact-topic Lean hit remains legacy `S1_M_050`; no new pinned external terminal declaration was found. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0134/StatementInfrastructure.lean` | 0 | The target-owned candidate vocabulary probe elaborated; it declares no canonical theorem. |
| `cd Formalizations/Lean && LC_ALL=C TZ=UTC lake env lean --trust=0 AwesomeTheorems/Stage1/S1_M_050.lean` | 0 | The legacy statement shape and conditional package elaborated without producing a terminal proof. |
| `python3 -m json.tool Stage1_Instances/THM-M-0134/anchor-audit-revalidation-blocker-20260717-slot89.json` | 0 | The structured blocker is valid JSON. |
| `git diff --check -- Stage1_Instances/THM-M-0134 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Expected post-edit integration boundary: the new target-owned blocker changes the generated theorem-DAG evidence inventory. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Same expected projection drift; only the master lane may regenerate the checked-in DAG. |

## Retry Condition

The scheduler/master lane must refresh the sole declared validator and the
target-owned ledger, inventory bindings, and exactly one phase receipt against
one current graph/base, then commit them before issuing a fresh claim whose
base contains that unchanged validator blob. The statement predecessor must be
separately master-accepted `[x]` before this phase can pass topology. A fresh
worker may write the self-test handoff only after the unchanged exact argv
returns a typed result that proves the phase predicate.

This is target-scoped revalidation blocker evidence only. It does not self-test
or accept `S56-M-0134-ANCHOR_AUDIT`, replace its historical receipt, refresh the
ledger, change task state, transfer provider acceptance, prove the root, claim
`AUDIT-Z` or `THEOREM-Z`, or claim master acceptance.
