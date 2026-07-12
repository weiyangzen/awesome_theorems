# Intake validation

Base revision: `ed278d07d4b1fbd48887625b78d32141bebc9441`.

Validation ran in the worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were used read only; no update, build, clone, or fetch command was used. This validation
covers manifest membership, dossier structure, JSON integrity, and a narrow pinned Lean API probe.
Because the repository record does not identify a proposition, it supplies no canonical expression
hash, mutation certificate, source acceptance, or proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0726` | exit 0; rank 763, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0726/instance.json >/dev/null` | exit 0; instance JSON parsed successfully |
| `python3 -m json.tool Stage1_Instances/THM-M-0726/task-dag.json >/dev/null` | exit 0; task DAG JSON parsed successfully |
| scoped Python intake assertions | exit 0; identity, planned lifecycle, null target, empty acceptance, open dependency chain, and owned-file invariants passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0726/IntakeProbe.lean)` | exit 0; six exact language, time/polytime, and PMF API types elaborated under Lean 4.29.0 |
| `! rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0726 -g '*.lean'` | exit 0; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0726` | exit 0; no whitespace errors |

Known downstream work remains open: exact source selection and review, target elaboration and
mutations, discovery and obligation freezes, proof, trust/provenance checks, hermetic replay,
independent verification, and master release acceptance. These boundaries prevent theorem
completion but do not invalidate a truthful `planned` intake.
