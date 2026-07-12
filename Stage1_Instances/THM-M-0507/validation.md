# Intake validation

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

This validation covers target membership, the planned dossier, JSON integrity, source discovery,
and a narrow pinned Lean API probe. Since the source names a method rather than a proposition, no
canonical target, expression fingerprint, mutation result, or proof is claimed. The canonical
`.lake` artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0507` | exit 0; rank 881, planned, legacy artifacts unaccepted, theorem_complete false |
| `rg -n -C 8 'THM-M-0507\|哈代-李特尔伍德圆法\|堆垒数论的基本方法' Docs` | exit 0; only method-level metadata and explicitly open Stage0 fields found |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0507/IntakeProbe.lean)` | exit 0; all six circle/Fourier API checks elaborated under Lean 4.29.0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0507/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0507/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` for identity, lifecycle, null target/fingerprint, debt boundary, no accepted state, open ordered DAG, and artifact inventory |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0507 -g '*.lean'` | exit 1, expected no-match result; no prohibited placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0507` | exit 0; no output |

Known downstream work is intentionally open: select and independently review an exact source
theorem; elaborate and mutation-test it; freeze discovery and obligations; audit anchors; implement
proof and composition; and perform hermetic and independent release validation. Those open nodes do
not invalidate a truthful `planned` intake.
