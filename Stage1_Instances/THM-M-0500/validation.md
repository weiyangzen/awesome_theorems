# Intake validation

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

This validation covers manifest membership, planned dossier structure, JSON integrity, and a narrow
pinned Lean API probe. It does not freeze or validate a canonical Lean target and does not inspect
or accept any proof body. The canonical `.lake` symlink and its pinned artifacts were used
read-only; no update, build, clone, or fetch was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0500` | exit 0; rank 877, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0500/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0500/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; planned lifecycle, empty accepted states, open formal target, false terminal flags, ordered open DAG, and artifact presence checked |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0500/IntakeProbe.lean)` | exit 0; all five pinned API declarations elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0500 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom in owned Lean source |
| `git diff --check -- Stage1_Instances/THM-M-0500` | exit 0; no output |

Known downstream work is intentionally open: primary-source edition/page/assumption/errata review,
canonical expression elaboration and mutation tests, checked alternate transport, obligation and
discovery freezes, formal-anchor provenance/trust audit, proof acceptance, hermetic replay, and
release review. These prevent audit and theorem completion but do not invalidate a truthful
`planned` intake.
