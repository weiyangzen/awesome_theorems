# THM-M-1228 proof-phase blocker

Item: `S56-M-1228-PROOF`  
Date: `2026-07-12`  
Base revision: `3cb5c69018ebf704c6fd68f32aaece780d6bf542`

## Verdict

`blocked`: no eligible proof body for the exact Caffarelli-Kohn-Nirenberg
partial-regularity target exists in the repository or pinned mathlib closure.
The checked `ObligationTree.root_compose` only consumes the still-open
per-solution singular-measure conclusion. It does not prove that conclusion.

The first failed proof gate is `M1228-S-CONCRETE`. The canonical statement is
a semantic interface because pinned mathlib has no concrete suitable weak
solution, CKN regular-point, or parabolic Hausdorff-measure API. Its three
predicates contain no conclusion witness. They also cannot be treated as
arbitrary assumptions: a semantics can make `IsSuitableWeakSolution` true and
`ParabolicHausdorffOneMeasureZero` false, so a generic proof would be invalid.

The frozen root cut remains `M1228-S-CONCRETE`, `M1228-E-EPSILON`,
`M1228-C-COVER`, and `M1228-L-MEASURE`. Closing it requires concrete PDE and
anisotropic-measure definitions, compactness/decay and epsilon regularity,
the bad-cylinder covering argument, and the terminal parabolic Hausdorff
measure proof. Neither the historical abstract package nor any audited
external candidate supplies those bodies. No premise, axiom, placeholder,
weaker measure, smooth-solution substitute, or two-dimensional theorem was
added.

Because the assigned proof phase is not self-tested complete, this attempt
deliberately does not create `.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone. The existing
`Formalizations/Lean/.lake` entry reuses the canonical pinned artifacts and was
not modified. No Lake update/build, dependency clone/fetch, or network action
was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | Rank 156, planned, hard-mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1228/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges pass; denominator `25704bee664136645e0481ae7d6273ac3fdfd2f1cd20fc5f82ba43f07066f41e`; root remains M4 with four open cut obligations. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1228/Statement.lean` | 0 | The canonical semantic-interface proposition elaborates under Lean 4.29.0. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1228/ObligationTree.lean` | 0 | Conditional root composition elaborates; `#print axioms` reports `[propext, Classical.choice, Quot.sound]`. It does not inhabit the per-solution premise. |
| `rg -n -i -e 'CaffarelliKohnNirenbergTarget' -e 'Caffarelli.Kohn.Nirenberg' -e 'SuitableWeakSolution' -e 'ParabolicHausdorff' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | 94 matching lines occur in only three files: this dossier's statement/harness and the historical abstract `S1_M_156` surface. No terminal exact proof body appears in pinned mathlib. |
| `rg -n '^\\s*(sorry\\|admit\\|axiom)(\\s\\|$)' Stage1_Instances/THM-M-1228 --glob '*.lean'` | 1 | No prohibited Lean declaration token occurs in the owned Lean sources; exit 1 means no match. |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |

Machine status remains M4 and theorem completion remains false. The pre-existing
untracked `.lake` link also means this is nonrelease evidence.
