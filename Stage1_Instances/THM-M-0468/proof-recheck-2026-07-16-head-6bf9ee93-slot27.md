# THM-M-0468 proof-phase recheck at current base

Item: `S56-M-0468-PROOF`

Base revision: `6bf9ee93a322e7d25cf9249226222095f95d1cff`

Base tree: `24acf86e69ab2e6fca9480c6269b6429874ba295`

## Verdict

`blocked`. No consistent positive proof body can inhabit the exact frozen Lean
target. `Statement.lean` quantifies over every `BogomolovData`, but that
structure imposes no laws connecting its carriers, operations, height,
density, torsion, or geometric predicates. The unchanged placeholder-free
declaration

```text
Stage1Instances.THM_M_0468.not_bogomolovTarget :
  Not Stage1Instances.THM_M_0468.BogomolovTarget
```

was replayed at trust level zero against the pinned Lean and mathlib artifacts.
Its singleton model makes every ambient hypothesis and density claim true,
sets canonical height to zero, and makes every torsion claim false. The frozen
target would therefore produce an `IsSpecial` torsion witness of `False`.

This refutes only the unconstrained abstract encoding, not the mathematical
Ullmo--Zhang theorem. A source-faithful repair must use concrete geometry or
substantive, noncircular compatibility laws. Such a repair belongs to the
statement phase and invalidates the current statement fingerprint and proof
architecture.

The checked `root_of_direction_packages` declaration remains conditional on
both missing implications, so it supplies no positive root proof credit. The
proof item remains `[ ]`; `root_closed=false`, `audit_complete=false`, and
`theorem_complete=false`. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Dependency Context

The complete v2 closure was traversed before this proof recheck. THM-M-0468 has
no direct hard parents, transitive hard ancestors, incoming hard edges, reuse
hints, or shared groups. `dependency-reuse-ledger.json` records that audited
empty closure under schema `stage1-dependency-reuse-ledger/1.1`, graph digest
`73e99d22...f40eca`, context digest `068170c7...c5c`, and this worker's exact
base revision. There is no provider proof credit to import or reject.

## Validation

All commands ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No update, build,
clone, fetch, network operation, or dependency mutation was performed. All
Lean outputs were written under a fresh `/tmp` directory and removed by trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-0468` | 0 | Rank 314, planned lifecycle, theorem incomplete. |
| `timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0468/check_statement.py` | 0 | Exact fingerprint `def6574c...fa0e`; the four recorded predicate-removal mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0468/check_anchor_audit.py` | 0 | Exact target/pin/module hashes and four candidate classifications passed. |
| `python3 Stage1_Instances/THM-M-0468/check_obligation_tree.py` | 0 | 20 obligations and 44 typed edges passed; denominator `0b324115...6c4`; root remains open M4. |
| `python3 -m json.tool dependency-reuse-ledger.json` plus `scripts.stage1_execution_cron.validate_dependency_reuse_ledger(...)` | 0 | Schema, graph/context/base bindings, and every required empty context list passed. |
| Isolated trust-zero `lake env lean` replay | 0 | Exact statement, conditional assembler, countermodel, and probe elaborated; both declarations were sorry-free; axioms were `[propext, Classical.choice, Quot.sound]`. |
| `rg -n` prohibited-token scan over target Lean sources | 1 | Expected no-match exit; no `sorry`, `admit`, axiom, unsafe, external, or equivalent proof escape was found. |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | Pre-existing authoritative drift: checked-in theorem DAG differs from fresh deterministic generation. |
| `python3 Docs/tools/check_stage1_standard.py` | 1 | Fails through the same pre-existing v2 DAG regeneration mismatch. |

The isolated object hashes were `ceaf7430...c689` (statement),
`5d46f876...7841` (conditional tree), `a4afb48a...c17` (countermodel), and
`6c60263d...ad13` (probe). The temporary directory was confirmed absent after
the replay.

The structural validator failure is recorded rather than repaired because
`Docs/Stage1_Theorem_DAG_v2.json` and its generator are outside this worker's
owned path and must not be edited by a proof worker.

## Retry Boundary

The first semantic failure is exact-target consistency at
`M0468-S-DOMAINS`; the actionable cut also includes the statement phase, both
direction packages, and the root. Reopen `S56-M-0468-STATEMENT`, replace the
unconstrained semantic surface, freeze and accept a new exact fingerprint and
registry version, then rerun statement mutations, anchor audit, obligation
tree, and proof execution in dependency order.

This is target-owned, current-base nonrelease blocker evidence. It claims no
proof completion, provisional state, accepted receipt, audit completion,
theorem completion, or master acceptance.
