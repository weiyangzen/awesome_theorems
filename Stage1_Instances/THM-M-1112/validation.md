# Intake validation

Base revision: `694b331243d16cc36a69b54661f4bcbd9813e120`.

Validation is limited to target membership, manifest consistency, dossier structure, scoped intake
invariants, and whitespace. The working tree already contained the unrelated untracked
`Formalizations/Lean/.lake` link before this task. No canonical Lean expression exists, so there is
no relevant `lake env lean` elaboration check and no kernel result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1112` | exit 0; rank 552, planned, L0/rework_required, theorem_complete false |
| `rg -n -i 'Erd[oő]s.?R[eé]nyi\|random graph\|随机图' Formalizations Docs ...` | exit 0; repository metadata found; Lean hits were only the unrelated THM-M-1009 second-lemma target |
| `python3 -m json.tool Stage1_Instances/THM-M-1112/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1112/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1112` | exit 0; no output |

Known downstream failures: the repository phrase does not identify a unique theorem; primary-source
inspection and independent review, the `G(n, m)`/`G(n, p)` decision, canonical Lean elaboration,
formal-anchor audit, obligation registry, proof, hermetic replay, and release validation remain
open. These failures prevent theorem completion but do not invalidate a truthful planned intake.
