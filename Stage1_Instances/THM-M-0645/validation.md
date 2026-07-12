# Intake validation

Base revision: `5112156d97b95a4c9f8dfb2a249eadfc0ba09442`.

Validation is limited to target-set consistency, dossier syntax, scoped intake invariants, and
whitespace. The exact source conventions and concrete derivation calculus are not selected, so a
Lean declaration at this phase would test an invented or broadened substitute. No elaboration,
kernel closure, source review, audit completion, or theorem completion is claimed. The existing
untracked `Formalizations/Lean/.lake` entry was present at preflight and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0645` | exit 0; rank 691, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0645/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0645/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; identity, lifecycle, rank, empty acceptance, debt vector, owned inventory, and ordered open DAG checked |
| direct trailing-whitespace/EOF assertion over owned files | exit 0; `owned text check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0645` | exit 0; no output |

Statement-phase validation is now recorded separately in `statement-validation.md`. Known
downstream failures remain: pinpoint primary-source inspection and independent review,
formal-candidate audit, obligation registry, proof, trust/provenance closure, hermetic replay, and
independent validation. They prevent every later phase and theorem completion but do not invalidate
the truthful planned lifecycle or the self-tested statement handoff.
