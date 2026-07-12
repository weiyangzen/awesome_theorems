# THM-M-1269 proof-phase validation

Item: `S56-M-1269-PROOF`. Base revision:
`c198d8dd5bd64a4d487ed7455874705d67fd300f`.

## Implemented proof body

`Proof.lean` proves the exact frozen `THM_M_1269_statement`. It applies the
pinned mathlib theorem `exists_seq_tendsto_sInf` to the nonempty bounded-below
range of `F`, chooses an `X`-preimage of every resulting range value, and
transports convergence across the pointwise equality. This installs a real,
unconditional root proof body and closes the frozen proof route through
`M1269-L-SINF`; it does not claim later validation, release, or theorem
completion gates.

## Commands and results

Validation ran on 2026-07-12. The existing canonical pinned `.lake` artifacts
were reused through the worker symlink. No update, build, dependency clone,
fetch, or mutation of `.lake` was performed.

```text
cd Stage1_Instances/THM-M-1269
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
rm -f Statement.olean
python3 check_proof.py
  exit 0: exact root elaborated; `#print axioms` reported `propext`,
  `Classical.choice`, and `Quot.sound`; structural and prohibited-device scans
  passed

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95

(cd Formalizations/Lean && lake env lean --version)
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-1269
  exit 0: rank 445, planned, theorem_complete=false
```

The machine proof body is present, but the receipt is provisional worker
evidence. Master acceptance, the validation and release phases, H0/R0,
hermetic replay, and independent verification remain unclaimed.
