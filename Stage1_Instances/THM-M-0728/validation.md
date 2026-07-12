# Intake validation

Base revision: `d19d83e12b57432e75cbb1c35f4577d5b0645cf9`.

Validation ran in the worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were used read only; no update, build, clone, or fetch command was used. Validation covers
manifest membership, dossier structure, JSON integrity, scoped intake invariants, and a narrow Lean
API probe. It does not supply an exact statement fingerprint, source acceptance, mutation tests, or
proof evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0728` | exit 0; rank 765, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0728/instance.json >/dev/null` | exit 0; instance JSON parsed successfully |
| `python3 -m json.tool Stage1_Instances/THM-M-0728/task-dag.json >/dev/null` | exit 0; task DAG JSON parsed successfully |
| scoped Python intake assertions | exit 0; identity, planned lifecycle, null formal target, empty acceptance, open dependency chain, and owned-file invariants passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0728/IntakeProbe.lean)` | exit 0; `Language`, `Turing.TM2OutputsInTime`, and `Turing.TM2ComputableInPolyTime` elaborated under pinned Lean 4.29.0 |
| `! rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0728 -g '*.lean'` | exit 0; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0728` | exit 0; no whitespace errors |

Known downstream work remains open: independent primary-source inspection, exact protocol and
complexity definitions, canonical target elaboration and mutation tests, anchor audit, obligation
registry, proof, trust/provenance checks, hermetic replay, independent verification, and master
release acceptance. These boundaries prevent theorem completion but do not invalidate a truthful
`planned` intake.
