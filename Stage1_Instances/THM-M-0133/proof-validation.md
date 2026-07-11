# THM-M-0133 proof-phase validation

Item: `S56-M-0133-PROOF`

Base revision: `69e9d8064a5efa61619e7f8e639b1bf9203e61a8`

## Implemented bodies

`Proof.lean` checks the definitional identity between the frozen target and
mathlib's `FermatLastTheorem`, pins mathlib's exponent-four theorem, and checks
the exact composition from all odd-prime exponent cases to the frozen target.
The composition consumes the odd-prime family as an explicit premise. It is
therefore not an unconditional proof of Fermat's Last Theorem.

The first unresolved machine gate is `M0133-B-ODD`: the local pinned closure
does not provide every odd-prime exponent case. The deeper Frey curve,
semistable modularity, and level-lowering obligations remain open. The root
remains `M2`, and `theorem_complete` remains false.

## Commands and results

Validation ran from the worker clone on 2026-07-12 (Asia/Shanghai). The existing
pinned `.lake` artifacts were reused. No dependency update, build, clone, or
fetch was run.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0133
  exit 0: rank 22, planned, L0/rework_required, theorem_complete=false

cd Stage1_Instances/THM-M-0133
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0: the target identity reported `[propext]`; exponent four and exact
  conditional composition reported `[propext, Classical.choice, Quot.sound]`
rm -f Statement.olean

python3 Stage1_Instances/THM-M-0133/check_proof.py
  exit 0: required proof bodies and explicit odd-prime premise passed

python3 Stage1_Instances/THM-M-0133/check_obligation_tree.py
  exit 0: 38 obligations and 40 typed edges passed; root remains open at M2

git diff --check -- Stage1_Instances/THM-M-0133 .stage1-worker-selftest.json
  exit 0: no whitespace errors
```

This is worker self-test evidence for the proof phase only. Source/readability
review, validation and release receipts, independent verification, and master
acceptance remain open.
