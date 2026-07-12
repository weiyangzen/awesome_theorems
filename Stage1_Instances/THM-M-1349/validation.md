# Intake validation

Base revision: `562c428c3d520ab42bba305174b7cad9409d7c0b`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a unique proposition, no canonical
target, expression hash, mutation result, source acceptance, or proof is claimed. The shared
canonical `.lake` artifacts were used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1349` | exit 0; rank 875, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1349/IntakeProbe.lean)` | exit 0; five pinned ODE, flow, periodic-point, derivative, and rectangular-divergence APIs elaborated under Lean 4.29.0 |

The remaining JSON, scoped invariants, prohibited-construct scan, and whitespace checks are recorded
after finalization in `intake-receipt.json`. These checks validate a truthful `planned` intake only.
All dependent phases and master acceptance remain open.
