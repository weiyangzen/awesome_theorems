# Obligation-tree validation

Validation date: 2026-07-12. Base revision: `48a1d632cacabc75bca90db155d57ebb777aee3d`.
Commands ran inside this worker clone and reused the existing pinned `.lake` artifacts. No dependency
update, fetch, build, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Stage1_Instances/THM-M-1010/build_obligation_artifacts.py` | 0 | deterministically wrote 15 registry rows and all typed graph projections |
| `python3 Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | structural checks and narrow Lean elaboration passed; 15 obligations and 31 typed edges |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered target manifest passed |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | rank 290 and uniform L0/rework status confirmed |
| `python3 -m json.tool` on the four generated JSON artifacts | 0 | every structured artifact parsed |
| `rg -n '\bsorry\b|\badmit\b|\baxiom\b|sorryAx' Stage1_Instances/THM-M-1010 --glob '*.lean'` | 1 expected | no forbidden Lean construct found |
| `git diff --check -- Stage1_Instances/THM-M-1010 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The checker compiles `Statement.lean` to a temporary directory with `lake env lean`, then compiles
`ObligationTree.lean` against that temporary object and deletes it. Its axiom print reports only
mathlib's expected `propext`, `Classical.choice`, and `Quot.sound`, with no custom axiom or
`sorryAx`. This validates the architecture node, not the open coupling package or the theorem.
