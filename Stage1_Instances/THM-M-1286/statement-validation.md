# Statement validation record

Item: `S56-M-1286-STATEMENT`  
Base revision: `b18a08591e70d8b29ed5ebb3f76a33bb76ca1f83`.

## Frozen target

`Stage1Instances.THM_M_1286.PolyaSzegoTarget` freezes the intake-selected finite-`p`, whole-space
claim. Sobolev membership is encoded without an invented library API: the function and an explicit
distributional weak gradient are both `MemLp`, with the gradient identity tested against every
smooth compactly supported scalar function. The existential rearrangement is nonnegative,
radial-antitone, and equimeasurable at each positive superlevel. Its weak-gradient `eLpNorm` is no
greater than the input gradient's norm. `polyaSzegoTarget_iff_expandedTarget` checks the fully
expanded spelling by definitional equality. No proof of the inequality is supplied.

## Commands and results

Lean commands ran from `Formalizations/Lean` against the existing pinned environment. No dependency
update, build, fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1286/Statement.lean` | 0 | root, expanded transport, and four scope mutations elaborated; explicit root printed |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-1286/Statement.lean lean-toolchain lake-manifest.json` | 0 | `ef428b...9bb`, `651c8a...1d2`, `321626...2d81` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique uniform-L0/rework-required targets |
| `python3 scripts/stage1_target.py show THM-M-1286` | 0 | rank 457, planned, theorem incomplete |

The separately named mutations remove the dimension boundary, admit `p = infinity`, remove the
finite-superlevel condition, or reverse the energy inequality. They elaborate as alternate
propositions and receive no proof credit. The exact source pinpoint, anchor audit, proof,
independent validation, and master acceptance remain open.
