# Intake validation

Base revision: `30d893623b4b974bbae53b781eacf4f8b4391787`.
Base tree: `f0431efd42feb3992395686e1f15453b41c84f38`.

Validation is limited to repository/manifest consistency, dossier structure, a discovery-only Lean
API probe, scoped intake invariants, and whitespace. The pre-existing untracked
`Formalizations/Lean/.lake` link is the canonical pinned dependency reuse supplied to this worker;
it was not created or mutated by this intake. No canonical Lean target or proof is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0541` | exit 0; rank 598, L0/rework_required, planned, theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0541/IntakeProbe.lean` | exit 0; the three pinned adjacent API declarations elaborated |
| `python3 -m json.tool Stage1_Instances/THM-M-0541/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0541/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0541` | exit 0; no output |

Known downstream failures: an immutable pinpoint human source, exact coefficient and orientation
conventions, canonical target elaboration and mutation tests, formal anchor/provenance audit,
obligation registry, proof, hermetic replay, and independent review remain open. They prevent audit
and theorem completion but do not invalidate this fail-closed planned intake.
