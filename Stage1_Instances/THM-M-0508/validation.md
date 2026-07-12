# Intake validation record

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

Validation is scoped to target membership, planned-instance invariants, JSON syntax, pinned Lean
API discovery, forbidden proof escapes, and whitespace. It does not test or claim an exact
Vinogradov statement, an analytic proof, source acceptance, or master acceptance. The canonical
`.lake` link and pinned artifacts were used read-only; no update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0508` | 0 | rank 882; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0508/instance.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0508/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python intake assertions | 0 | IDs, rank, lifecycle, inventory, empty accepted state, open downstream tasks, and absent formal-target/completion claims agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0508/IntakeProbe.lean)` | 0 | pinned environment elaborated prime, parity, eventual-filter, and prime-counting APIs |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0508 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0508 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The Lean output is genuine elaboration evidence for statement-building APIs only. Known downstream
failures remain deliberately open: immutable pinpoint source and errata review, exact statement and
expression fingerprint, all four mutation classes, formal-candidate audit, obligation/discovery
freezes, proof, composition and trust closure, readable reconstruction, hermetic replay, independent
validation, and master acceptance. They prevent theorem completion but do not invalidate this
truthful `planned` intake.
