# Intake validation

Base revision: `128997c29e0211f5c45f2205b13ff707daad37d6`.

Validation is limited to target membership, repository-standard consistency, dossier structure,
JSON syntax, scoped intake invariants, and whitespace. There is no canonical Lean expression in
this phase, so no elaboration or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1083/instance.json >/dev/null` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1083/task-dag.json >/dev/null` | exit 0 |
| scoped Python dossier and intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets at ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1083` | exit 0; rank 525, `planned`, `L0/rework_required`, historical artifacts unaccepted, theorem incomplete |
| prohibited proof-shortcut token scan over the five substantive dossier files | exit 1 as expected; no matches |
| `rg -n '[ \t]+$' Stage1_Instances/THM-M-1083` | exit 1 as expected; no trailing whitespace |

Known downstream failures are the primary-source pinpoint and review, exact Lean statement and
mutation checks, immutable anchor audit, frozen obligation registry, proof construction or
integration, hermetic replay, and independent release verification. These open gates prevent
theorem completion but do not invalidate an honest `planned` intake.
