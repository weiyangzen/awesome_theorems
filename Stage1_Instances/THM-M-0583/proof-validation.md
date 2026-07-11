# THM-M-0583 proof-phase blocker

Item: `S56-M-0583-PROOF`  
Date: `2026-07-12`  
Base revision: `046b0721abb228d13c7042349574736fe375cd97`

## Verdict

`blocked`: no eligible proof body for the exact four-dimensional topological
Poincare target exists in the repository or pinned mathlib closure. The checked
declaration `canonicalRoot_of_freedmanTopologicalCore` is only a conditional
adapter: its argument is definitionally the complete target, so it supplies no
part of Freedman's proof.

The first failed proof gate is `M0583-X-FREEDMAN-CORE`. Its machine-critical
subtree still requires homotopy-invariant reduction, a compatible topological
model, disk embedding, topological surgery, four-dimensional topological
s-cobordism, and construction of the final homeomorphism. Pinned mathlib has
only the `proof_wanted` source marker. The audited external candidates either
prove only dimension zero or use `sorry` for dimension four, and neither is a
pinned dependency. No premise, axiom, placeholder, or weaker theorem was added.

Because the assigned proof phase is not self-tested complete, this attempt does
not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone. The existing `Formalizations/Lean/.lake`
entry points to the canonical pinned artifacts and was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes with 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0583` | 0 | Rank 116, lifecycle `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0583/check_obligation_tree.py` | 0 | 16 obligations, 32 typed edges, seven graph kinds; denominator `910aad119639e1751b6f8c0ad6d04f98a030acdc0e00c951cd46f6efff18cccd`; root open M2. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0583/Statement.lean` | 0 | The exact canonical target elaborates with Lean 4.29.0. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0583/ObligationTree.lean` | 0 | The conditional adapter elaborates; its axiom report is `[propext, Classical.choice, Quot.sound]`. It does not construct `FreedmanTopologicalCore`. |
| `rg -n -i -e 'nonempty_homeomorph_sphere' -e 'fourDimensionalTopologicalPoincareTarget' -e 'FreedmanTopologicalCore' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Hits are owned statement/adapter declarations, legacy audit strings, and mathlib's source-level `proof_wanted`; no terminal proof body was found. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0583 --glob '*.lean'` | 1 | No prohibited Lean declaration token was found; exit 1 means no match. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

The toolchain reported Lean commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`. No Lake update, build, dependency
clone, fetch, or `.lake` mutation was performed. Machine status remains M2 and
theorem completion remains false.
