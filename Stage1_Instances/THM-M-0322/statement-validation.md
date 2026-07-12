# Statement validation record

Item: `S56-M-0322-STATEMENT`  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`

## Frozen target

`Stage1Instances.THM_M_0322.KreinMilmanTarget` universally quantifies the exact ambient structures
used by the pinned mathlib declaration: a real module with additive commutative group, Hausdorff
topology, continuous addition and scalar multiplication, and real local convexity. For every set
`s`, compactness and real convexity imply
`closure (convexHull Real (s.extremePoints Real)) = s`.

The sole direct import is `Mathlib.Analysis.Convex.KreinMilman`. The theorem
`kreinMilmanTarget_of_pinned` checks that `closure_convexHull_extremePoints` inhabits the frozen
universal target. This wrapper identifies the target boundary; provenance and trust inspection of
the upstream proof body remain the dependent anchor-audit node's work.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` against the
existing pinned Lake environment; no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0322/Statement.lean` | 0 | exact target, pinned wrapper, four mutations, and empty-set boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-0322/check_statement.py` | 0 | expression SHA-256 `785719abddfc881edb6ec8cb60f1175995b433ae42f12727d7d3a1479955579f`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Stage1_Instances/THM-M-0322/Statement.lean Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | hashes `8f66eb...4732`, `651c8a...1d2`, and `321626...5cb2`, matching `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0322` | 0 | rank 819, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0322/statement.json` | 0 | statement receipt JSON valid |
| `git diff --check -- Stage1_Instances/THM-M-0322` | 0 | no whitespace errors |

## Mutation and boundary policy

The validator compares serialized explicit elaborated expressions. It rejects removal of
compactness, specialization of the arbitrary ambient space to `Real`, moving compactness outside
the set binder, and adding nonemptiness. The last mutation protects the degenerate-case boundary:
`empty_boundary` separately checks the equality for the empty set through the pinned declaration.

This is statement-only evidence pending master acceptance. It does not advance anchor-audit,
obligation-tree, proof, validation, or release nodes and does not claim theorem completion.
