# THM-M-0161 proof-phase attempt

Item: `S56-M-0161-PROOF`  
Date: `2026-07-12` (`Asia/Shanghai`)  
Base revision: `89d346c6e4d70a887dc4caa607fa8e82a9050b47`

## Verdict

`blocked`: no eligible proof body for the exact fundamental theorem of space curves exists in the
repository or pinned dependency closure. No proof body was added and no proof credit is claimed.

The immediate root cut remains the exact `M0161-T-EXISTENCE` and `M0161-T-UNIQUENESS` packages.
The first unavailable construction is `M0161-C-FRENET-LOCAL`: an actual time-dependent Frenet ODE
solution from the frozen differentiability and positivity hypotheses. Pinned mathlib's
Picard-Lindelof and ODE uniqueness theorems are ingredients, not this construction. A proof must
still encode the system, establish its hypotheses, preserve an oriented orthonormal frame, extend
the solution over the arbitrary open interval, integrate its tangent, recover the exact within
derivatives and invariants, and prove determinant-one rigid-motion uniqueness.

`ObligationTree.lean` has the real proof body
`root_of_existence_and_uniqueness`, but it is only conditional composition: both complete packages
are inputs. Treating it as root closure would broaden the theorem's premises. The prerequisite
anchor audit also found no exact pinned external proof; its only relevant external development has
explicit `sorry` bodies and lacks the prescribed-invariants theorem. Postulating either package
would violate the no-placeholder rule. Root debt therefore remains `M4`, `root_closed=false`, and
`theorem_complete=false`.

Because the assigned proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately
absent.

## Narrow validation evidence

All checks ran in this worker clone and reused the canonical pinned Lake artifacts. No `lake
update`, `lake build`, clone, fetch, or dependency mutation was performed. A temporary local
`Statement.olean` used solely to resolve the dossier-local `import Statement` was removed after the
check.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0161` | 0 | rank 660; planned; L0/rework-required; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0161/check_obligation_tree.py` | 0 | 21 obligations and 44 typed edges passed; denominator `48173f90...a43060`; exact existence and uniqueness packages remain open |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0161/Statement.lean` | 0 | exact canonical proposition elaborated and printed |
| dossier-local `lake env lean` invocation with the pinned `LEAN_PATH` for `Statement.lean` then `ObligationTree.lean` | 0 | conditional composition elaborated; `#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i 'fundamental theorem of (space )?curves\|prescribed (curvature\|torsion)\|frenet.?serret\|signed torsion' Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching repository or pinned mathlib source declaration |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum` on statement, conditional assembly, registry, Lake manifest, and toolchain | 0 | `82f74a6f...43060`; `137db71e...cf7d7`; `d080078c...ae3da`; `321626c8...2d81`; `651c8acc...1d2` |

## Reopen condition

Resume after a placeholder-free implementation of the frozen global Frenet construction and both
exact terminal packages, or discovery of an immutable compatible Lean 4 proof that can be pinned,
exact-type transported, and validated in the repository closure.
