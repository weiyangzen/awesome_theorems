# Intake validation

Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Since the needed subfactor-index interface and source boundary are open, no
canonical expression, mutation result, or proof is claimed. The clone's canonical `.lake` artifact
was used read-only; no update, build, clone, or fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0335` | exit 0; rank 828, planned, legacy artifacts not accepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0335/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0335/task-dag.json` | exit 0 |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0335/IntakeProbe.lean` | exit 0; all five pinned von Neumann algebra API checks elaborated |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0335` | exit 0; no output |
| placeholder scan of owned Lean files | exit 0; no `sorry`, `admit`, or `axiom` token |

Known downstream failures are deliberately open: pinpoint primary-source theorem/page and errata,
independent source review, restriction-versus-realization and boundary decisions, a type `II_1`
factor/subfactor/index Lean interface, canonical elaboration and mutation tests, anchor audit,
obligation registry, proof, hermetic replay, and independent validation. These prevent theorem
completion but do not invalidate this self-tested fail-closed planned intake.
