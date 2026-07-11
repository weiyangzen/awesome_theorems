# THM-M-0010 proof-phase validation

## Implemented proof

`Proof.lean` imports the exact target frozen in `Statement.lean` through an
isolated temporary `Statement.olean`. The theorem
`Stage1Instances.THM_M_0010.Proof.artinRees` discharges that target with the
pinned mathlib body `Ideal.exists_pow_inf_eq_pow_smul`, using the same ordered
universes, typeclasses, ideal, module, submodule, witness, lower-bound guard,
and equality. No premise or conclusion was broadened or substituted.

The source contains no `sorry`, `admit`, new axiom, `sorryAx`, or unsafe
declaration. Lean reports only `propext`, `Classical.choice`, and `Quot.sound`
in the wrapper's axiom closure. This is provisional proof-node evidence;
master acceptance, validation, and release remain open, and theorem completion
is not claimed.

## Commands and exact results

Commands ran from base revision
`41a639c14626145f43eda7724d6a570cd710d688` on 2026-07-12 (receipt timestamp
`2026-07-11T23:24:08Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0010
  exit 0: execution rank 103; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0010/check_proof.sh
  exit 0: isolated Statement.olean and Proof elaboration passed;
  artinRees reports propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0010/check_proof.py
  exit 0: exact frozen target, pinned terminal declaration, registry root,
  statement hash, and prohibited-token checks passed

python3 Stage1_Instances/THM-M-0010/check_obligation_tree.py
  exit 0: PASS with 10 frozen obligations and denominator
  cad255358d70a3800a3c8cc01487f3fd885892841121614567e7c739d109a9cc

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
temporary directory and isolated `.olean` were deleted by the command trap.
