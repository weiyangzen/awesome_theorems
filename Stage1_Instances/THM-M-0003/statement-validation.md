# Statement validation record

Item: `S56-M-0003-STATEMENT`  
Base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`

## Frozen target

`Stage1Instances.THM_M_0003.SnakeLemmaTarget` quantifies over an arbitrary abelian category and one
`ShortComplex.SnakeInput`. That input packages the commuting four-row diagram, its componentwise
kernel and cokernel witnesses, exact middle rows, and the epi/mono assumptions at the middle-row
ends. The conclusion is exactness of precisely the six-term sequence
`L0.X1 -> L0.X2 -> L0.X3 -> L3.X1 -> L3.X2 -> L3.X3`.

The sole direct import is `Mathlib.Algebra.Homology.ShortComplex.SnakeLemma`, the defining module for
the object model used in the proposition. `PointwiseSnakeLemmaTarget` changes only the grouping of
the category binder, and `snakeLemmaTarget_iff_pointwise` checks that transport in Lean. This phase
does not invoke or inspect the proof declaration `ShortComplex.SnakeInput.snake_lemma`.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake environment; no dependency or `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0003/Statement.lean` | 0 | canonical target, checked transport, and four structural mutations elaborated; fully explicit canonical expression printed |
| `python3 ../../Stage1_Instances/THM-M-0003/check_statement.py` | 0 | expression SHA-256 `1132689414bcc557fc2a760263e8a3b3a656272a59254a642ad999f6a244ca40`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Stage1_Instances/THM-M-0003/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `d6a0a1...8cece`, `651c8a...b1d2`, and `321626...2d81`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0003` | 0 | rank 98, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Mutation and scope boundary

The validator compares fully explicit elaborated expressions. It distinguishes removal of the
entire snake diagram and its packaged hypotheses, a changed category universe, moving existence of
a snake input into the conclusion, and adding endpoint assumptions associated with a stronger
zero-extended sequence. These are statement-identity checks; they do not claim each mutation is a
false proposition.

This is statement-only evidence pending master acceptance. It does not establish an anchor audit,
proof closure, H0, M0, audit completion, independent validation, or theorem completion.
