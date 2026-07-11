# THM-M-0442 proof attempt

Item: `S56-M-0442-PROOF`  
Date: `2026-07-12`  
Base revision: `8ee975c34c2703e7a7490329d73c6615458b9295`

## Verdict

`blocked`: the exact theorem has no eligible proof body in the repository or
the pinned mathlib closure. The existing `ObligationTree.engine_compose` checks
only the implication from an inhabitant of `MazurEngine`; no such inhabitant
exists. Supplying one would require closing the eleven mathematical leaves
listed in `proof-blocker.json`, including compactified modular-curve rational
points and Mazur's arithmetic descent.

No proof source was added, no weaker theorem was substituted, and no axiom or
unproved declaration was introduced. Because the assigned proof phase is not
self-tested complete, this attempt deliberately does not create
`.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone unless the command explicitly changes
to `Formalizations/Lean`. The existing `.lake` entry is the canonical pinned
artifact symlink and was not modified.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0442` | 0 | Rank 88, planned, hard-mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0442/check_obligation_tree.py` | 0 | `PASS THM-M-0442 obligation freeze: 21 obligations, 20 proof edges; root open`. |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0442/Statement.lean` | 0 | Exact canonical proposition elaborates under Lean 4.29.0. |
| `(Statement.lean + ObligationTree.lean without its import line) \| lake env lean /dev/stdin` from `Formalizations/Lean` | 0 | Conditional `engine_compose` elaborates; `#print axioms` reports only `propext`, `Classical.choice`, and `Quot.sound`. This does not inhabit `MazurEngine`. |
| `rg -n -i 'MazurRationalTorsionTarget\|MazurTorsionClassified\|Mazur_statement\|rational torsion classification' --glob '*.lean' Stage1_Instances Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Matches are confined to this dossier, the historical statement/consequence file, and metadata about the weaker external axiom; no terminal classification proof body was found in pinned mathlib. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)' Stage1_Instances/THM-M-0442` | 1 | No prohibited Lean declaration token found; exit 1 means no match. |

The available toolchain is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; `lake-manifest.json` pins mathlib
at `8a178386ffc0f5fef0b77738bb5449d50efeea95`. No update, build, clone, fetch,
or dependency mutation was run.
