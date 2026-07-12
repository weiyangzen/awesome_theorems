# THM-M-1245 proof-phase validation

Item: `S56-M-1245-PROOF`. Base revision:
`3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`.

`Proof.lean` closes frozen terminal obligation `M1245-A-TERMINAL` by applying
the pinned mathlib declaration
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner`. It checks the Euclidean
finrank and exponent transports explicitly. The named root proof then uses the
already checked uniform-constant bridge, closing `M1245-ROOT` at the proof-body
level without changing the frozen statement.

Validation ran from the worker clone on 2026-07-12. Existing pinned Lake
artifacts were reused; no dependency update, build, clone, or fetch was run.

```text
cd Stage1_Instances/THM-M-1245
export ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0
BASE_LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)"
LEAN_PATH="$BASE_LEAN_PATH" lake env lean -o Statement.olean Statement.lean
LEAN_PATH=".:$BASE_LEAN_PATH" lake env lean -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$BASE_LEAN_PATH" lake env lean Proof.lean
  exit 0
  auditedTerminalEstimate_proof depends on axioms:
    [propext, Classical.choice, Quot.sound]
  sobolevInequalityTarget_proof depends on axioms:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean
  exit 0; no generated olean remains under the owned path

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-1245
  exit 0: rank 326, planned, theorem_complete false
python3 Stage1_Instances/THM-M-1245/check_proof.py
  exit 0: PASS THM-M-1245 proof phase: terminal and exact root proof bodies installed
python3 -m json.tool Stage1_Instances/THM-M-1245/proof-receipt.json
  exit 0
rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b|^[[:space:]]*unsafe\b' \
  Stage1_Instances/THM-M-1245/Proof.lean
  exit 1 with empty output: pass, no prohibited declaration or placeholder
git diff --check -- Stage1_Instances/THM-M-1245 .stage1-worker-selftest.json
  exit 0; no output
```

This provisional proof receipt establishes exact kernel-elaborated root proof
bodies for the assigned phase. It does not claim theorem completion: the
validation and release nodes, human-source H0, readable R0, hermetic replay,
provenance, independent verification, and master acceptance remain open.
