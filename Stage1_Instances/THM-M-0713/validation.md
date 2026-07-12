# Intake validation

Base revision: `f4c286c4ebc4a8b1a5d0a746afd6fba9849e4c7c`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository gloss does not uniquely choose among three materially
different propositions, no canonical target, expression hash, mutation result, source acceptance,
or root proof is claimed. The pre-existing canonical `.lake` artifacts were used read-only; no
update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0713` | exit 0; rank 752, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0713/instance.json` | exit 0; intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0713/task-dag.json` | exit 0; open task DAG JSON is syntactically valid |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0713/IntakeProbe.lean)` | exit 0; `Poly`, `Dioph`, `DiophFn`, `Pell.matiyasevic`, `pell_dioph`, and `pow_dioph` elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0713 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0713` | exit 0; no output |

Known downstream failures are intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, natural/integer and computability transports,
obligation/discovery freeze, full anchor and provenance audit, proof, hermetic replay, and release
acceptance. They prevent theorem completion but do not invalidate a truthful `planned` intake.
