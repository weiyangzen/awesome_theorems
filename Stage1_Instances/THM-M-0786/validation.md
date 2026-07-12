# Intake validation

Base revision: `444819795285695894ff7b29af5c2419e0e000fa`.

Validation ran in the worker clone on 2026-07-12 (Asia/Shanghai). The canonical pinned `.lake`
artifacts were reused read only; no update, build, clone, or fetch command was used. The untracked
`Formalizations/Lean/.lake` link was present before this dossier was created and is not an owned
artifact. Validation covers target-set consistency, dossier structure, JSON integrity, scoped
intake invariants, and only the Lean vocabulary needed to show that a future statement can refer to
Baire-space-shaped plays and measurable payoff sets. It does not elaborate Borel determinacy.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0786` | exit 0; rank 791, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0786/instance.json >/dev/null` | exit 0; instance JSON parsed |
| `python3 -m json.tool Stage1_Instances/THM-M-0786/task-dag.json >/dev/null` | exit 0; task DAG JSON parsed |
| scoped Python intake assertions | exit 0; identity, planned lifecycle, null formal target, empty acceptance, open dependency chain, and owned-file invariants passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0786/IntakeProbe.lean)` | exit 0; `Nat -> Nat`, payoff sets, the topology, measurable space, and `MeasurableSet` elaborated under pinned Lean 4.29.0/mathlib |
| `! rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0786 -g '*.lean'` | exit 0; no prohibited placeholder or axiom in the Lean probe |
| `git diff --check -- Stage1_Instances/THM-M-0786` | exit 0; no whitespace errors |

An initial pre-validation run of the scoped assertion script exited 1 because it checked the
declared owned-file list before this `validation.md` file had been created. No mathematical or Lean
gate failed; the identical final script passed after the dossier became complete.

Known downstream work remains open: immutable primary-source inspection and independent review,
exact game/strategy/topology statement elaboration and mutation tests, formal-candidate audit,
obligation freeze, proof, trust and provenance closure, hermetic replay, and independent release
verification. These gates prevent theorem completion but do not prevent a truthful `planned`
intake.
