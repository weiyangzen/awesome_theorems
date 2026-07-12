# Intake and statement validation

Statement worker base revision: `15209c0db1b16388f976ffb2244cadfdd6f3866d`.

Statement validation uses the existing pinned Lean and mathlib artifacts. The canonical declaration,
its definitional expansion, and four deliberately altered statement shapes elaborate; the validator
compares explicit elaborated expressions and confirms that no mutation is identical to the target.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-1245` | exit 0; rank 326, L0/rework_required, planned, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1245/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1245/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-1245` | exit 0; no output |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1245/Statement.lean` | exit 0; canonical target elaborated and printed |
| `python3 Stage1_Instances/THM-M-1245/check_statement.py` | exit 0; expression SHA-256 `de06a2c7...d6125e80`; four mutations killed; mathlib `8a178386...eea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1245/statement.json` | exit 0 |

Known downstream failures: primary-source pinpointing and attribution review, anchor and terminal
proof-body audit, obligation registry, proof acceptance, hermetic replay, and independent review
remain open. They prevent proof credit and theorem completion but do not invalidate this
fail-closed, statement-only result.
