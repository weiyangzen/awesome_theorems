# Intake validation

Base revision: `2ff2721a0184cf5f856054cb7d46b10dbc703f5a`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, source acceptance, or proof is claimed. The shared canonical
`.lake` link and artifacts were used read-only; no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0704` | exit 0; rank 745, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0704/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0704/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0704/IntakeProbe.lean)` | exit 0; `Lean.Expr.bvar`, `Lean.Expr.lam`, and `Lean.Expr.app` elaborated under Lean 4.29.0 |
| `! rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0704 -g '*.lean'` | exit 0; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0704` | exit 0; no output |

## Status boundary

Known downstream work is intentionally open: exact source selection and independent review,
canonical statement elaboration and mutation tests, discovery and obligation freezes, formal-anchor
audit, proof, hermetic replay, and release acceptance. Those prevent theorem completion but do not
invalidate a truthful, self-tested `planned` intake.
