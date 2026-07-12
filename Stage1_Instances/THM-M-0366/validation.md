# Intake validation

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

This validation covers target membership, planned-dossier structure, JSON integrity, bounded source
and pinned-mathlib discovery, and a narrow pinned Lean API probe. Because the exact primary theorem
has not been inspected, no canonical Lean expression, mutation result, singular-integral operator,
proof, or anchor closure is claimed. The pre-existing canonical `.lake` artifacts were used
read-only; no update, build, clone, or fetch command was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0366` | exit 0; rank 858, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0366/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0366/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0366/IntakeProbe.lean)` | exit 0; all eight Lipschitz, integral, and `L^p` API checks elaborated |
| `rg -n -i 'coifman\|mcintosh\|meyer\|cauchy (integral\|transform)\|lipschitz.*cauchy' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 0; ordinary circle Cauchy-integral results and unrelated names found, but no recognizable CMM or Lipschitz-curve singular-integral declaration |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0366 -g '*.lean'` | exit 1 as expected for no matches; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0366 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures are exact primary theorem/page and errata inspection, independent source
review, canonical statement elaboration and mutation tests, singular-integral encoding, discovery
and obligation freezes, proof, hermetic replay, and release acceptance. They prevent theorem
completion but do not invalidate this truthful `planned` intake.
