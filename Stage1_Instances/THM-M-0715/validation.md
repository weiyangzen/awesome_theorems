# Intake validation

Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record names a field rather than a proposition, no canonical
target, expression hash, mutation result, source acceptance, or proof is claimed. The pre-existing
canonical `.lake` artifacts were used read-only; no update, build, fetch, or clone was run.

All results below are evidence for intake only.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0715` | exit 0; rank 754, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0715/instance.json` | exit 0; intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0715/task-dag.json` | exit 0; open task DAG JSON is syntactically valid |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0715/IntakeProbe.lean)` | exit 0; all eleven representative recursive-function, enumerability, halting, and Turing-machine declarations elaborated |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0715 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0715` | exit 0; no output |

Known downstream failures are intentionally open: primary source selection and independent review,
canonical statement elaboration and mutation tests, computation-model transports, obligation and
discovery freezes, formal-anchor and provenance audit, proof, hermetic replay, and release
acceptance. They prevent theorem completion but do not invalidate a truthful `planned` intake.
