# Intake validation

Base revision: `3a479c703900e8096e6b239e7bf5b0da25472b8a`.

Validation ran in the worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were read only; no update, build, clone, or fetch command was used. This validation covers
manifest membership, dossier structure, JSON integrity, and a narrow pinned Lean API probe. Since
the source record does not identify a proposition, it supplies no canonical expression hash,
mutation certificate, source acceptance, or proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0719` | exit 0; rank 758, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0719/instance.json >/dev/null` | exit 0; instance JSON parsed successfully |
| `python3 -m json.tool Stage1_Instances/THM-M-0719/task-dag.json >/dev/null` | exit 0; task DAG JSON parsed successfully |
| scoped Python intake assertions | exit 0; identity, planned lifecycle, null target, empty acceptance, open dependency chain, and owned-file invariants passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0719/IntakeProbe.lean)` | exit 0; four exact time/polytime API types elaborated under Lean 4.29.0 |
| `! rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0719 -g '*.lean'` | exit 0; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0719` | exit 0; no whitespace errors |

Known downstream work remains open: exact source selection and review, target elaboration and
mutations, discovery and obligation freezes, proof, trust/provenance checks, hermetic replay,
independent verification, and master release acceptance. These boundaries prevent theorem
completion but do not invalidate a truthful `planned` intake.
