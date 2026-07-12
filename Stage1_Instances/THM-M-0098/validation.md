# Intake validation

Base revision: `028e2535b68678b8296e63e2cacb05ed9775a2d8`.

Validation date: `2026-07-12` (`Asia/Shanghai`). This validation covers target membership, dossier
structure and fail-closed intake invariants, JSON integrity, and a narrow pinned Lean API probe. The
canonical `.lake` artifacts were reused read-only; no update, build, clone, or fetch was run. The
pre-existing untracked `Formalizations/Lean/.lake` link is outside this target and was not modified.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0098` | exit 0; rank 899, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0098/instance.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0098/task-dag.json` | exit 0; valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0098/intake-receipt.json` | exit 0; valid JSON after receipt finalization |
| `python3 Stage1_Instances/THM-M-0098/check_intake.py` | exit 0; IDs and rank agree, lifecycle is planned, canonical claim/expression/hash are null, provisional vector is H5/M4/R4, accepted state is empty, all six downstream tasks are open and dependency ordered, source literals and artifact inventory agree, and both completion booleans are false |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0098/IntakeProbe.lean)` | exit 0; six adjacent scheme, Galois, Haar-measure, local-field, adele, and representation APIs elaborated under Lean 4.29.0 |
| `rg -n '\\b(sorry\\|admit)\\b\\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0098 -g '*.lean'` | exit 1 as expected; no prohibited proof placeholder or axiom found |
| `git diff --check -- Stage1_Instances/THM-M-0098 .stage1-worker-selftest.json` | exit 0; no whitespace errors |

The Lean probe does not elaborate a canonical target and supplies no proof credit. Known failures
are the unresolved catalog title/gloss identity, absent immutable source selection and independent
review, null formal target and expression fingerprint, unfrozen discovery and obligation hashes,
and every downstream statement, anchor, tree, proof, release, hermetic-replay, and independent
verification gate. These failures prevent statement and theorem completion but do not invalidate a
truthful self-tested `planned` intake.
