# THM-M-0406 validation validator-authority blocker

## Scope

This is the target-scoped fail-closed result for `S56-M-0406-VALIDATION` at worker base
`d41a1ade92426e33aade0ff4e796cd5b4da27a44` (tree
`c592c028b1d440807661d791cf10af9f4dd08331`). It changes no theorem source, prior phase receipt,
task-state authority, theorem-DAG projection, lifecycle, debt vector, or acceptance state.

The assigned claim order is `(v2_execution_rank=258, phase_layer=5,
phase_item_id=S56-M-0406-VALIDATION)`. The complete `parent_inspection_order` is empty. The
authoritative theorem node has no direct hard parent, transitive hard ancestor, hard edge, reuse
hint, or shared-lemma group, so no provider proof body, receipt, or acceptance was consumed or
transferred.

## First failed gate

`G05-AUTHORITY-REPLAY / validator_candidate_missing` is the first mechanically unrepairable worker
gate. The HEAD validation contract declares exactly these scheduler-owned candidates:

- `Stage1_Instances/THM-M-0406/check_validation.py`
- `Stage1_Instances/THM-M-0406/check_validation.sh`

Neither path exists in the worker base or at current `HEAD`. The mandatory selection rule requires
exactly one candidate already present at the worker base, with its HEAD blob unchanged. The worker
is expressly forbidden to create, refresh, rename, replace, or delete a validator candidate.
Consequently there is no authority-selected argv to run and no possible stdout object with schema
`stage1-validator-semantic-result/1.0`. Exit-zero structural or Lean checks cannot substitute for
that typed semantic result.

Per the phase contract and worker instructions, this scheduler-ownership defect prevents a genuine
validation self-test. Therefore this run deliberately emits no `validation-receipt.json` and no
`.stage1-worker-selftest.json`.

## Dependency and prerequisite boundary

The current target-owned `dependency-reuse-ledger.json` has the required
`stage1-dependency-reuse-ledger/1.1` shape and truthfully records the empty closure, but it is a
proof-phase historical ledger bound to graph digest
`eaee68bdf9fde9e311db076d1997fd8ef91919def0ba0fb399f1df77080f7153` and revision
`94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`. The current graph digest is
`7c81855adb1d19b7be5dd3dfbbb41dd441b3dc17021d08471909b28018881962`, while the stable dependency
context remains `068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c`.
It is not refreshed here because a validation ledger that claims a completed consumer self-test
would be false without the scheduler-owned validator and required receipt.

Independent of that mechanical blocker, `G02-TOPOLOGY` and the positive validation predicate also
fail:

- `S56-M-0406-PROOF` is authoritative `[_]`, not master-accepted `[x]`.
- Its current `stage1-node-receipt/1.0` is `accepted=false`, `verdict=blocked`, and proves no positive
  root closure.
- `Proof.lean` instead kernel-checks
  `Stage1Instances.THMM0406.not_corvajaZannierTheoremOne` at `k = Rat`: the frozen abstract
  `SurfaceData` permits `curve := Empty` while every premise is satisfiable.
- All fourteen frozen positive machine obligations remain open, and the minimal root cut set
  includes `M0406-S-DEFINITIONS` and `M0406-ROOT`.
- The current encoding is therefore refutable; this says nothing against the mathematical
  Corvaja-Zannier theorem and supplies no positive proof or validation credit.

Thus `audit_complete=false` and `theorem_complete=false`. No accepted receipt ID, phase acceptance,
M0, AUDIT-Z, THEOREM-Z, release grade, or theorem-completion claim is supported.

## Bounded checks

The following checks were run from the worker root on 2026-07-17 (Asia/Shanghai):

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 structure, target set, v2 graph, and contract checks passed |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 nodes, 10822 states, and the acyclic typed graph passed |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and validator ownership rules passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique L0/rework-required targets passed |
| `python3 scripts/stage1_target.py show THM-M-0406` | 0 | rank 19 target remains planned and theorem-incomplete |
| validation-candidate enumeration from the HEAD contract and Git tree | 0 | exactly zero declared candidates exist for this target |
| trust-zero scratch replay of `Statement.lean` and `Proof.lean` using `lake env which lean` and the existing `LEAN_PATH` | 0 | exact statement elaborated; both countermodel declarations reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `git diff --check -- Stage1_Instances/THM-M-0406` | 0 | no whitespace errors |

The Lean replay copied the two unchanged sources to `/tmp` and reused the automation-provided
canonical pinned `.lake` symlink read-only. No `lake update`, build, clone, fetch, network access, or
dependency-cache mutation was performed. These checks establish coherent target-scoped negative
evidence only; they are not the missing scheduler-selected semantic validator replay.

## Retry condition

The scheduler/master lane must publish exactly one HEAD-tracked validation validator at a declared
candidate path, then issue a fresh `S56-M-0406-VALIDATION` claim whose immutable worker base contains
that exact blob. Positive validation will still remain blocked until the invalid statement encoding
is reopened and replaced with a source-faithful, noncircular proposition, its exact statement and
obligation tree are reaccepted, a placeholder-free positive proof is master accepted, and the new
validator replay establishes every required kernel, trust, provenance, reuse, and independent
validation gate.
