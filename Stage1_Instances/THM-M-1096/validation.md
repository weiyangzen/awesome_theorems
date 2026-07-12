# Intake validation

Base revision: `e545899c85e870efdef04615348353d8d5552315`.

The preflight worktree contained the repository-provided untracked symlink
`Formalizations/Lean/.lake` to the canonical pinned artifacts. It was inspected but not modified.
This is nonrelease intake evidence.

Validation is limited to target-set consistency, dossier structure, source-metadata retrieval,
scoped assertions, and whitespace. No canonical Lean proposition exists yet, so running an
unrelated Lean theorem would provide no statement evidence and no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1096` | exit 0; rank 536, planned, L0/rework_required, theorem_complete false |
| `curl -L --max-time 20 -s 'https://api.crossref.org/works?query.title=Ergodic%20properties%20of%20recurrent%20diffusion%20processes%20and%20stabilization&rows=3'` | exit 0; publisher deposit returned DOI `10.1137/1105016`, volume 5(2), pages 179-196, 1960 |
| `rg -n -i 'khasmin\|hasmin\|invariant.*measure\|ergodic.*diffusion\|stationary.*distribution' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/AwesomeTheorems` | exit 0; general invariant/ergodic APIs found, no Khasminskii name or identified terminal recurrent-diffusion theorem |
| `python3 -m json.tool Stage1_Instances/THM-M-1096/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1096/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1096` | exit 0; no output |

The final JSON, invariant, and diff checks are recorded after dossier creation. Known downstream
failures are exact primary-source inspection, canonical Lean elaboration and mutations, anchor
audit, frozen obligation graphs, proof, hermetic validation, and independent review. These block
theorem completion but do not invalidate this fail-closed planned intake.
