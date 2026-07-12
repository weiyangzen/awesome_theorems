# Intake validation

Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`.

This validation covers target membership, planned-dossier structure, JSON integrity, and a narrow
pinned Lean API probe. It does not establish source fidelity, canonical statement identity, proof
provenance, or theorem completion. The pre-existing canonical `.lake` artifacts were used read-only;
no update, build, fetch, or clone was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0342` | exit 0; rank 835, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0342/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0342/task-dag.json` | exit 0; valid JSON |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0342/IntakeProbe.lean)` | exit 0; the linear isometry, norm theorem, inner-product theorem, and scalar Euclidean specialization elaborated under Lean 4.29.0 |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0342 -g '*.lean'` | exit 1 as expected; no prohibited placeholder or axiom matched |
| `git diff --check -- Stage1_Instances/THM-M-0342` | exit 0; no output |

Known downstream failures are intentionally open: primary-source passage and independent review,
normalization decisions, canonical expression and mutation tests, obligation/discovery freezes,
terminal-body and trust audit, proof acceptance, hermetic replay, and release validation. They
prevent theorem completion but do not invalidate a truthful `planned` intake.
