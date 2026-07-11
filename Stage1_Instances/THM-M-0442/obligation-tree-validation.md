# THM-M-0442 obligation-tree validation

Date: 2026-07-12

Base revision: `de00e2ad5f81be2e2d8c539b9959c341720761d0`

## Results

1. `python3 Stage1_Instances/THM-M-0442/check_obligation_tree.py`
   - Exit 0.
   - `PASS THM-M-0442 obligation freeze: 21 obligations, 20 proof edges; root open`
2. `(cat ../../Stage1_Instances/THM-M-0442/Statement.lean; tail -n +2 ../../Stage1_Instances/THM-M-0442/ObligationTree.lean) | lake env lean /dev/stdin`
   - Run from `Formalizations/Lean`; exit 0 using the pinned toolchain and existing `.lake` closure.
   - Printed `engine_compose : MazurRationalTorsionTarget` and the ordinary axiom
     footprint `[propext, Classical.choice, Quot.sound]`.
   - Concatenation is used only because the dossier is outside the Lake source
     root; it elaborates the unchanged statement followed by the unchanged
     obligation module with its local `import Statement` line omitted.
3. `git diff --check -- Stage1_Instances/THM-M-0442`
   - Exit 0; no whitespace errors.

The Lean run checks only the conditional composition term. `MazurEngine` is not
inhabited, no mathematical obligation is closed, and the theorem remains open.
