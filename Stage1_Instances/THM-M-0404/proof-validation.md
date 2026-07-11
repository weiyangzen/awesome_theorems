# THM-M-0404 proof-phase validation

Item: `S56-M-0404-PROOF`. Base revision:
`66de3677bc74fc1d4856dbd3ee3d83f3815ecd12`.

This proof phase adds a real local proof of the frozen
`M0404-L-COMBINATORIAL` package and composes it with the still-explicit
`EventuallyPeriodicZeroSets` premise. It does not assert the number-theoretic
Skolem-Mahler-Lech package or claim root/theorem completion.

Validation ran from the worker clone on 2026-07-12. The existing canonical
pinned `.lake` artifacts were reused through the worker symlink; no update,
build, dependency clone, or fetch was run.

```text
cd Stage1_Instances/THM-M-0404
LEAN_PATH="$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o Statement.olean Statement.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean \
    -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH)" \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 lake env lean Proof.lean
  exit 0
  eventualPeriodic_to_finiteUnion depends on axioms:
    [propext, Classical.choice, Quot.sound]
  root_of_eventuallyPeriodicZeroSets depends on axioms:
    [propext, Classical.choice, Quot.sound]
rm -f Statement.olean ObligationTree.olean

python3 Docs/tools/check_stage1_standard.py
  exit 0: ok; 15 assurance groups, 1546 uniform-L0 targets
python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required
python3 scripts/stage1_target.py show THM-M-0404
  exit 0: rank 17, planned, theorem_complete false
python3 Stage1_Instances/THM-M-0404/check_proof.py
  exit 0: PASS THM-M-0404 proof phase: local combinatorial package closed; root remains conditional
git diff --check -- Stage1_Instances/THM-M-0404 .stage1-worker-selftest.json
  exit 0; no output
```

The proof uses finite lists of the true residues below the positive period,
and `Function.Periodic.map_mod_nat` to reduce every tail index to its residue.
The exact remaining machine cut set begins with
`M0404-T-EVENTUAL`: `EventuallyPeriodicZeroSets` is still an explicit premise.
No placeholder, axiom declaration, unsafe declaration, or substituted target
is present. Master acceptance remains required.
