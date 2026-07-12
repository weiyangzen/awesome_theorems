# Intake validation

Base revision: `6f601f70dc531aafc2c0e73ea51db67cebeb3ad9`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record does not identify a proposition, no canonical target,
expression hash, mutation result, or proof is claimed. The shared canonical `.lake` artifacts were
used read-only and were not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0375` | exit 0; rank 867, planned, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0375/IntakeProbe.lean)` | exit 0; all seven pinned harmonic-analysis API checks elaborated under Lean 4.29.0 |

The JSON, scoped intake invariants, forbidden-token scan, and whitespace checks are recorded after
finalization in `intake-receipt.json`. Known downstream failures remain intentionally open: exact
source selection and review, canonical statement elaboration and mutation tests, obligation and
discovery freezes, anchor audit, proof, hermetic replay, and release acceptance. They block theorem
completion but do not invalidate a truthful `planned` intake.

