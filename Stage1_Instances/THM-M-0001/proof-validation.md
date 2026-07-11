# THM-M-0001 proof-phase validation

## Implemented proof

`Proof.lean` imports the exact target frozen in `Statement.lean`. Its canonical
wrapper applies the pinned mathlib bodies `ShortExact.homology_exact₂`,
`homology_exact₃`, and `homology_exact₁` at every degree and every
`ComplexShape.Rel` pair. This closes the same-degree and both connecting-map
positions without truncating the continuing sequence.

The proof has no `sorry`, `admit`, new axiom, unsafe declaration, or substituted
target. Lean reports only `propext`, `Classical.choice`, and `Quot.sound` in its
axiom closure. Proof execution is self-tested pending master acceptance;
validation and release remain separate nodes, so theorem completion is not
claimed.

## Commands and results

Commands ran from base revision
`cd5c49706246d0b87fcaae19ae75214b45f66a85` on 2026-07-12 (receipt timestamp
`2026-07-11T22:50:52Z` UTC).

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0001
  exit 0: execution rank 96; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0001/check_proof.sh
  exit 0: isolated Statement.olean and Proof elaboration passed; the wrapper
  reports propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0001/check_proof.py
  exit 0: exact frozen target and all three expected mathlib bodies found;
  prohibited source-token scan passed

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

No update, build, clone, fetch, or mutation of `.lake` was performed. The
isolated `.olean` was deleted by the command trap.
