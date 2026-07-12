# THM-M-1333 proof-phase validation

Item: `S56-M-1333-PROOF`. Base revision:
`e9d545372b66f73be63271b2fb408ef134d1d6f7`.

## Implemented body

`Proof.lean` closes the frozen `M1333-L-ZERO-DIM` obligation. For state space
`Fin 0 -> Real`, it takes the constant initial-state curve. Openness of `U`
along the continuous map `t |-> (t, x0)` supplies a positive time ball; half
its radius contains the requested closed interval. Subsingleton elimination
identifies both `f t x0` and the derivative of the constant curve with zero.
The same module closes the exhaustive dimension branch and exact assembly
interfaces: given the explicitly still-open positive-dimensional result, it
splits on `n = 0` and derives the unchanged `PeanoExistenceTarget`.

This is genuine partial proof progress only. The positive-dimensional
delayed-Euler and Arzela-Ascoli route remains open, so the canonical root stays
at `M4` and theorem completion is false.

## Commands and results

Validation ran in the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no update, build, fetch, clone, or `.lake` mutation was
performed.

```text
python3 Stage1_Instances/THM-M-1333/check_proof.py
  exit 0
  peanoExistence_fin_zero depends on axioms:
    [propext, Classical.choice, Quot.sound]
  peanoExistenceTarget_of_positive_dimension depends on axioms:
    [propext, Classical.choice, Quot.sound]

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1333
  exit 0: rank 874, planned, theorem_complete false

rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-1333/Proof.lean
  exit 1 with empty output: pass

python3 -m json.tool Stage1_Instances/THM-M-1333/proof-receipt.json
  exit 0: valid JSON

git diff --check -- Stage1_Instances/THM-M-1333 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

The remaining mathematical cut is the entire positive-dimensional route:
approximation construction and invariants, compact extraction, passage to the
integral equation, endpoint derivative recovery, and exact root composition.
The assembly interface itself is checked; its positive-dimensional premise is
the remaining input preventing root closure. No stronger-hypothesis
Picard-Lindelof result is substituted for that debt.
