# Intake validation

Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`.

Validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned Lean
API probe. The canonical `.lake` link and artifacts were used read-only; no update, build, fetch, or
clone was run. Because source inspection and exact statement identity remain open, this is not a
canonical-target elaboration, proof check, or anchor audit.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0329` | exit 0; rank 822, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0329/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0329/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0329/IntakeProbe.lean)` | exit 0; coercivity and three Lax-Milgram candidate declaration types elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0329 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0329` | exit 0; no output |

Known downstream open gates are exact primary-source theorem/page inspection and independent
review, canonical statement elaboration and mutation tests, obligation/discovery freeze, candidate
provenance and trust audit, proof evidence acceptance, hermetic replay, and release validation.
They prevent theorem completion but do not invalidate a truthful `planned` intake.
