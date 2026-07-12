# THM-M-0769 validation-phase result

Item: `S56-M-0769-VALIDATION`  
Base revision: `5314165df54baa70993fddf08cc142a9739a74e0`  
Validation time: `2026-07-12T09:33:18Z`

The node-scoped validator replayed the exact frozen statement, conditional
composition, proof-phase selector and root, and a separately written direct
root in a fresh temporary directory. `Validation.lean` imports only
`Statement`; it imports neither `Proof` nor `ObligationTree` and uses the core
`Pi.instNonempty` route rather than the proof's explicit pointwise
`Classical.choice` term. This is same-worker differential evidence, not
rev-5.6 independent verification.

## Exact result

```text
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 \
  python3 Stage1_Instances/THM-M-0769/check_validation.py
  exit 0
  PASS narrow kernel replay: exact statement, frozen composition, proof root, and differential direct root elaborated
  PASS trust observation: proof and differential roots report exactly Classical.choice; conditional composition is axiom-free
  PASS local provenance: statement, anchor, registry, graph, proof receipt, toolchain, and clean mathlib pin agree
  STALE frozen graph: the pre-proof graph retains an M3 root and open fiber-choice node pending master reconciliation
  BLOCKED hermetic gate: shared warm canonical .lake was reused; no cold empty-cache offline replay or complete TCB/SBOM archive
  BLOCKED independent gate: differential source ran in this worker and shared cache, not a distinct signed runner

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0769
  exit 0: rank 779, planned, L0/rework_required, theorem_complete false
```

The validator invoked `lake env lean` against existing pinned Lean 4.29.0 and
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. It copied sources
into a fresh temporary directory under `Formalizations/Lean`, emitted only a
temporary `Statement.olean`, and removed the directory. It performed no
update, build, clone, fetch, network operation, or dependency mutation. The
pinned mathlib worktree was clean.

## Gate decisions

| Gate | Decision | Evidence or failure |
|---|---|---|
| Narrow kernel replay | pass | The exact statement, conditional composition, proof root, and separately implemented direct root elaborate. |
| Placeholder/unsafe scan | pass | Five checked Lean modules contain no `sorry`, `admit`, `sorryAx`, local `axiom`, or `unsafe` declaration. |
| Trust observation | provisional pass | Proof and differential roots print exactly `Classical.choice`; conditional composition is axiom-free. A release-grade complete TCB profile is absent. |
| Local provenance | pass | Statement, anchor, registry, graph, proof receipt, toolchain, manifest, and clean mathlib revision hashes agree. |
| Structured-state freshness | fail closed / stale | The frozen pre-proof graph still reports an M3 root and open selector. Only the master may reconcile it. |
| Hermetic validation | fail closed | Shared warm `.lake`; no immutable clean checkout, cold empty-cache offline replay, full TCB inventory, or SBOM/license archive. |
| Independent verification | fail closed | The distinct implementation ran in this worker clone and cache; no separate identity, runner, signature, or independent minimal verifier exists. |

The first failed requested validation gate is `validation.hermetic_replay`.
This provisional receipt grants no `E0/E1`, accepted `M0-*`, `AUDIT-Z`,
`THEOREM-Z`, release, or master-acceptance credit. Human-source `H0` and
readable `R0` remain open, so `audit_complete=false` and
`theorem_complete=false`.
