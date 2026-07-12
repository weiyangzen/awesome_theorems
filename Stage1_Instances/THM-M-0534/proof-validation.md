# THM-M-0534 proof-phase validation

## Implemented proof

`Proof.lean` imports the exact target and frozen obligation composition. The direct wrapper applies
the pinned mathlib bodies `ShortExact.homology_exact₂`, `homology_exact₃`, and
`homology_exact₁` at every degree and every `ComplexShape.Rel` pair. A second theorem supplies
the same three families to `root_of_exactness_families`, checking the frozen child-to-parent route.

Both declarations close the exact root without `sorry`, `admit`, a new axiom, an unsafe declaration,
or a substituted target. Lean reports only `propext`, `Classical.choice`, and `Quot.sound`. Proof
execution is self-tested pending master acceptance; validation and release remain separate, so
theorem completion is not claimed.

## Commands and results

Commands ran from base revision `30d893623b4b974bbae53b781eacf4f8b4391787` on 2026-07-12.

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed

python3 scripts/stage1_target.py check
  exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required

python3 scripts/stage1_target.py show THM-M-0534
  exit 0: execution rank 591; planned; theorem_complete=false

cd Formalizations/Lean &&
  bash ../../Stage1_Instances/THM-M-0534/check_proof.sh
  exit 0: isolated Statement, ObligationTree, and Proof elaboration passed;
  both root declarations report propext, Classical.choice, and Quot.sound

python3 Stage1_Instances/THM-M-0534/check_proof.py
  exit 0: exact target, expected pinned bodies, composition route, and
  prohibited-token scan passed

python3 Stage1_Instances/THM-M-0534/check_obligation_tree.py
  exit 0: 14 obligations and 35 typed edges passed; the frozen pre-proof
  registry truthfully retains its M1 boundary

cd Formalizations/Lean && lake env lean --version
  exit 0: Lean 4.29.0, commit 98dc76e3c0a9b856c9b98726b713fb04fab16740

git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD
  exit 0: 8a178386ffc0f5fef0b77738bb5449d50efeea95
```

No update, build, clone, fetch, or mutation of `.lake` was performed. Temporary `.olean` files were
removed by the command trap. The first proof invocation exposed underspecified lambda binders in the
composition wrapper and exited 1; they were replaced with explicit binders, after which the exact
recorded recipe passed. That failed edit produced `sorryAx` only in the rejected elaboration output,
not in the accepted source or final kernel result.
