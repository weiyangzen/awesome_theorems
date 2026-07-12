# Intake validation

Base revision: `74980872e6ba4cca3e08b1b728b5cf3695421b94`.

The pre-existing untracked `Formalizations/Lean/.lake` path is the canonical pinned artifact link
reused by this worker. It was not created or mutated by this intake, and the run is nonrelease
evidence.

| Command | Result | Scope |
|---|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present | normative structure |
| `python3 scripts/stage1_target.py check` | exit 0: 1546 unique targets, ranks 1..1546, all L0/rework_required | manifest integrity |
| `python3 scripts/stage1_target.py show THM-M-0696` | exit 0: rank 737, planned, L0/rework_required, theorem_complete false | membership and target metadata |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0: Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release | pinned Lean executable availability; no theorem elaboration claimed |
| `python3 -m json.tool Stage1_Instances/THM-M-0696/intake.json >/dev/null` | exit 0 | dossier JSON syntax |
| `python3 -m json.tool Stage1_Instances/THM-M-0696/task-dag.json >/dev/null` | exit 0 | local open-DAG JSON syntax |
| `python3 - <<'PY' ... PY` (assert required files, IDs, planned lifecycle, open gate, seven open tasks, and `theorem_complete=false`) | exit 0: `dossier-local check: ok (5 required artifacts, planned, 7 open tasks, theorem_complete=false)` | dossier-local references and fail-closed state |
| `git diff --check -- Stage1_Instances/THM-M-0696` | exit 0 | whitespace integrity |

These checks self-test the intake deliverable only. No source-fidelity acceptance, Lean statement
gate, proof, kernel closure, or theorem completion is claimed. The next gate is master acceptance of
`S56-M-0696-INTAKE`; the dependent statement task remains open.
