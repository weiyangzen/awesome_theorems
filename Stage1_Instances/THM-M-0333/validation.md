# Intake validation

Base revision: `8014740e5a37eff82745f6fd2bc69f0ee45e67c9`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not freeze an exact source formulation, no
canonical target, expression hash, mutation result, or proof is claimed. The pre-existing canonical
`.lake` link and artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0333` | exit 0; rank 826, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0333/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0333/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; IDs/lifecycle/open states/null target/no accepted state/artifact inventory agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0333/IntakeProbe.lean)` | exit 0; nine relevant algebra, centralizer, bundled-von-Neumann-algebra, weak-operator-topology, and closure APIs elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry|admit)\b|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0333 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0333` | exit 0; no output |

Known downstream gates intentionally remain open: primary-source selection and independent review,
canonical statement elaboration and mutation tests, obligation and discovery freezes, exhaustive
anchor audit, proof, hermetic replay, and release acceptance. They prevent theorem completion but
do not invalidate a truthful `planned` intake.
