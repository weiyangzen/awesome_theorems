# Intake validation record

Base revision: `60fe286fb6a79de4164adae42c8b29610e7f5cde`.

Validation is scoped to target membership, planned-instance invariants, JSON syntax, the two Lean
API discovery anchors, forbidden proof escapes, and whitespace. It does not test or claim an exact
Page-theorem statement or proof.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0502` | 0 | rank 682; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0502/instance.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0502/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python assertions over `instance.json` and `task-dag.json` | 0 | `intake invariant check: ok`; IDs/rank/lifecycle agree, accepted states are empty, all downstream tasks are open, and no expression hash or completion claim exists |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0502/IntakeProbe.lean)` | 0 | pinned environment elaborated `DirichletCharacter.LFunction` and `DirichletCharacter.LFunction_ne_zero_of_one_le_re` |
| `rg -n '\b(sorry\|axiom)\b' Stage1_Instances/THM-M-0502 --glob '!validation.md'` | 1 | no matches; exit 1 is ripgrep's no-match result |
| `git diff --check -- Stage1_Instances/THM-M-0502` | 0 | no whitespace errors |

The Lean output exposes `LFunction` for `DirichletCharacter C N` (with `C` the complex numbers in
the pretty-printer) and proves the neighboring nonvanishing result only when `1 <= re s`, subject
to its principal-character exception. This is genuine kernel elaboration evidence for available
APIs, not root evidence.

Known downstream failures are deliberate and fail closed: the pinpoint primary statement and
errata review, exact constant and region, canonical Lean expression, statement mutations, formal
candidate audit, obligation registry, proof, source/readability review, hermetic replay, and
independent validation remain open. Master acceptance is also outstanding.
