# THM-M-0605 proof-phase attempt

Item: `S56-M-0605-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `b33312e792c156f58e747a0f53dfa36691ee0658`

## Verdict

`blocked`: no eligible proof body for the exact exotic seven-sphere target exists in the
repository or pinned dependency closure. The immediate root cut remains `M0605-T-WITNESS`, which
must supply one specific smooth seven-manifold, a homeomorphism to the standard topological
seven-sphere, and an `IsEmpty Diffeomorph` certificate. The first unavailable construction is
`M0605-C-BUNDLE`, the selected Milnor 3-sphere bundle over the 4-sphere with its required clutching
and characteristic data.

`ObligationTree.lean` contains the real proof body
`exoticSevenSphereExists_of_witness`, but it only checks terminal assembly after all three witness
components are passed as premises. It constructs none of them. The pinned mathlib source contains
only `proof_wanted exists_homeomorph_isEmpty_diffeomorph_sphere_seven`; as established by the
prerequisite anchor audit, that command leaves no declaration or proof body in the environment.
The bounded source search found no other relevant Lean theorem.

Therefore the bundle construction, total-space smooth structure, homotopy-sphere argument,
topological Poincare bridge, bounding eight-manifold, smooth obstruction computation, standard
sphere comparison, and non-diffeomorphism proof all remain open. Adding any of those as an axiom or
unproved premise would be a placeholder; returning the existing conditional assembly would
substitute a weaker theorem. Root debt remains `M4`, `root_closed=false`, and
`theorem_complete=false`. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Narrow validation evidence

All commands ran in this worker clone and reused the canonical pinned Lake artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0605` | 0 | rank 643; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0605/check_obligation_tree.py` | 0 | 19 obligations and 90 typed edges passed; denominator `c6e29bcc...b6e5b7`; root open M4 and witness construction open |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0605/Statement.lean` | 0 | exact canonical target elaborated and its explicit expression printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0605/ObligationTree.lean` | 0 | conditional assembly elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i` for exotic sphere, Milnor sphere, homotopy sphere, Eells-Kuiper, Poincare conjecture, and the exact marker in pinned mathlib | 0 | the sole hit was the known `proof_wanted` marker in `Geometry/Manifold/PoincareConjecture.lean:65` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `sha256sum` on the statement, conditional assembly, and registry | 0 | `7ee1cf3d...d1a31`; `62079890...9a0a`; `781157e8...91a0` |

## Reopen condition

Resume only after a placeholder-free implementation of the frozen Milnor construction and both
comparison branches, or discovery of an immutable compatible Lean 4 proof that can be pinned,
exact-type transported, and validated in the repository closure.
