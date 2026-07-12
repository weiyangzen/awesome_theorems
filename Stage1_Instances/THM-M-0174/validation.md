# Intake validation

Base revision: `ef32fd7c384b998c2d1505d21d9b5ea7940310b9`.

Validation is limited to target-set consistency, dossier syntax, scoped intake invariants, source
and formal-surface discovery, and whitespace. No canonical Lean expression has been selected in
this intake phase, so no elaboration or kernel-proof result is claimed. The existing
`Formalizations/Lean/.lake` symlink was already untracked at preflight; it points to the canonical
pinned artifacts and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0174` | exit 0; rank 668, L0/rework_required, planned, theorem_complete false |
| `rg -n -i 'hirzebruch\|signature theorem\|L-class\|L genus\|signature.*pontryagin\|希策布鲁赫' Formalizations Docs ...` | exit 0; found only generic/adjacent repository material and the Stage0 metadata; no theorem-specific Lean artifact |
| `rg -n -i 'hirzebruch\|signature theorem\|LClass\|lClass\|pontryagin.*signature\|signature.*pontryagin' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | exit 0 because incidental `*Class` substrings matched; inspection found no relevant Hirzebruch signature or `L`-class declaration; not a complete anchor audit |
| `python3 -m json.tool Stage1_Instances/THM-M-0174/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0174/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; checked identity, lifecycle, baseline, rank, empty acceptance, root vector, exact artifact set, ordered open DAG, and dependency chain |
| direct trailing-whitespace assertion over owned files | exit 0 |
| `git diff --check -- Stage1_Instances/THM-M-0174` | exit 0; no output (the dossier is untracked, so the direct assertion above checks its content) |

Known downstream failures: pinpoint primary-source inspection and independent review, exact source
conventions, canonical Lean elaboration and mutation tests, formal-candidate audit, obligation
registry and typed graphs, proof, hermetic replay, and independent validation remain open. They
prevent theorem completion but do not invalidate this fail-closed `planned` intake.
