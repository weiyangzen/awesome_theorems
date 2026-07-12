# THM-M-1524 obligation-tree validation

Validated on 2026-07-12 in the worker clone at base revision
`ddb0b11e29bb8010d71d71ef2061688eb61811cf`. Lean used only the existing pinned Lake
environment; no dependency update, build, clone, or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1524/build_obligation_artifacts.py` | 0 | deterministically wrote 14 obligations; denominator `f7589f32...0e2b` |
| `python3 Stage1_Instances/THM-M-1524/check_obligation_tree.py` | 0 | hashes, schema fields, denominator, 29 typed edges, reciprocity, proof reachability, acyclicity, leaf budgets, recipes, readable anchors, and open-root boundary passed; exact statement, mathlib Cauchy-Schwarz leaf, and conditional root composition elaborated; reported axioms were `[propext, Classical.choice, Quot.sound]` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets consistent |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets and ranks 1 through 1546 consistent |
| `python3 scripts/stage1_target.py show THM-M-1524` | 0 | rank 192, planned, L0/rework-required, theorem incomplete |
| `rg -n 'sorry\|admit\|axiom \|sorryAx' Stage1_Instances/THM-M-1524/ObligationTree.lean Stage1_Instances/THM-M-1524/build_obligation_artifacts.py` | 1 | expected no-match; no forbidden proof construct |
| `python3 -m json.tool` on all four new JSON artifacts | 0 | all structured artifacts parse |
| `git diff --check -- Stage1_Instances/THM-M-1524 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validator creates a temporary `Statement.olean` outside the repository, adds only that
temporary directory to `LEAN_PATH`, runs `lake env lean` on the owned tree module, and removes the
directory. It does not mutate `.lake`.

## Boundary

This phase freezes the objective denominator and validates conditional composition only. The
minimal open root cut set is `M1524-N-CENTER`, `M1524-L-SYMMETRY`, and
`M1524-L-CCR-SCALAR`; root status remains `M2`. There is no proof, audit, release, or
theorem-completion claim. Master acceptance is still required.
