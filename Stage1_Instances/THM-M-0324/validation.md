# Intake validation

Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`.

The pre-existing untracked `Formalizations/Lean/.lake` symlink exposes the canonical pinned build
artifacts and was not created or modified by this intake. This is nonrelease evidence. Validation
is limited to target-set consistency, dossier invariants, JSON syntax, and elaboration of the
Schauder-basis representation APIs in `IntakeCheck.lean`. Those API checks do not construct an
Enflo space, prove approximation-property failure, or prove the existential root.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0324` | exit 0; rank 820, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0324/IntakeCheck.lean` | exit 0; basis type, partial-sum projections, convergence, finite rank, uniform bound, and fixed-space basis/non-basis proposition shapes elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0324/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0324/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0324` | exit 0; no output |

Known downstream failures: publisher full-text retrieval was blocked during intake; exact Theorem 1
text, scalar convention, approximation-property definition, bundled existential Lean expression
and fingerprint, source review, exhaustive formal-candidate audit, obligation tree, proof,
composition, hermetic replay, and independent validation remain open. These are honest downstream
gates and prevent theorem completion; they do not invalidate a self-tested `planned` intake.

The later statement-phase validation is recorded separately in `statement-validation.md`. It
supersedes only the intake's open bundled-expression item: the selected conservative real target is
now elaborated and fingerprinted. The primary Theorem 1 text, approximation-property/reflexivity
transport, and every proof and release gate remain open.
