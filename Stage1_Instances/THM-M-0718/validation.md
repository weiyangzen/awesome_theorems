# Intake validation

Base revision: `136ebf643dcdcbc42cef34e415177189578060ef`.

This intake validation covers target membership, structured dossier integrity, and a narrow pinned
Lean API probe. It does not validate a canonical theorem statement or proof. The worker reused the
canonical `.lake` symlink read-only; it did not run dependency updates, builds, clones, or fetches.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0718` | exit 0; rank 757, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0718/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0718/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0718/IntakeProbe.lean)` | exit 0; all seven pinned computability/TM2 API checks elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0718` | exit 0; no output |

Known downstream failures are intentionally open: primary-source passage and independent review,
canonical statement and expression fingerprint, statement mutations, discovery and obligation
freezes, exact candidate crosswalk, proof and provenance closure, hermetic replay, and release
acceptance. They prevent theorem completion but do not invalidate a truthful `planned` intake.
