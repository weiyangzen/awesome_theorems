# THM-M-0667 validation-phase result

Item: `S56-M-0667-VALIDATION`  
Base revision: `bb6fb28ac1c55ecb52f3f1c84e7fbb35c26b47ad`  
Validation time: `2026-07-14T00:36:30+08:00`

The node-scoped validator replayed the exact statement, conditional
composition, proof wrapper, and a separately written root in a temporary olean
directory. `Validation.lean` imports only `Statement` and rebuilds the root
from `exists_lt_ack_of_nat_primrec`; it imports neither `Proof` nor
`ObligationTree` and does not invoke `not_primrec₂_ack`. This is same-worker
differential evidence, not rev-5.6 independent verification.

## Exact results

```text
python3 -B Stage1_Instances/THM-M-0667/check_validation.py
  exit 0
  PASS THM-M-0667 narrow kernel replay: exact proof root and differential root elaborated
  PASS THM-M-0667 trust observation: roots report propext, Classical.choice, Quot.sound
  PASS THM-M-0667 local provenance: frozen hashes and clean pinned mathlib source agree
  STALE structured state: pre-proof graph remains M3 pending master reconciliation
  BLOCKED hermetic gate: shared warm .lake; no cold empty-cache offline replay or full TCB archive
  BLOCKED independent gate: differential probe shared this worker checkout and cache

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0667
  exit 0: rank 711, planned, L0/rework_required, theorem_complete false
python3 -B Stage1_Instances/THM-M-0667/check_obligation_tree.py
  exit 0: 16 obligations, 36 typed edges; conditional composition elaborated
python3 -B Stage1_Instances/THM-M-0667/check_statement.py
  exit 0: exact expression hash matched; four structural mutations were killed
```

The validator derived `lean` and `LEAN_PATH` with `lake env`, copied the five
Lean sources into a temporary directory under the owned path, and removed it
after the run. It performed no update, build, clone, fetch, network operation,
or dependency mutation. The mathlib worktree was clean at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | Exact proof root and separately implemented domination-based root elaborate at the frozen target. |
| Placeholder/unsafe scan | pass, scoped | Five local Lean modules and the pinned terminal source contain no prohibited proof mechanism; parser-aware transitive closure remains open. |
| Trust observation | provisional pass | Both roots report exactly `propext`, `Classical.choice`, and `Quot.sound`; complete foundation-policy and TCB review is absent. |
| Local provenance | pass | Frozen source/registry/graph/proof hashes, terminal source, remote, revision, tree, compiled module, license, and clean dependency state agree. |
| Dependency acceptance | fail closed | `S56-M-0667-PROOF` is only worker-self-tested, not master-accepted. |
| Structured-state freshness | fail closed / stale | The frozen pre-proof graph still reports root `M3`; only the master may reconcile it. |
| Hermetic validation | fail closed | Shared warm `.lake`; no immutable clean checkout, cold empty-cache offline replay, full TCB archive, or network isolation. |
| Independent verification | fail closed | The distinct implementation ran in this worker clone and cache; no separate identity, runner, signature, or independent minimal verifier exists. |

Receipt `S56-M-0667-VALIDATION-local-20260714T003630+0800` is provisional,
nonrelease worker evidence. The first dependency-ordered acceptance failure is
proof master acceptance; the first failed requested validation gate is cold
hermetic replay. Primary-source `H0`, independently accepted `R0`, `AUDIT-Z`,
`THEOREM-Z`, release, and master acceptance remain open. No theorem-completion
claim is made.
