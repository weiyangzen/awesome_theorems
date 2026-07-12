# Intake validation

Base revision: `230f719da7724afb27c761dcb8c62a327557fe63`.

This validation covers manifest membership, dossier structure, JSON integrity, and a narrow pinned
Lean declaration probe. It does not elaborate a canonical target or inspect proof closure. The
pre-existing shared canonical `.lake` artifact was used read-only; no dependency update, fetch, or
build was run.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0343` | exit 0; rank 836, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-0343/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0343/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok`; IDs, lifecycle, open canonical claim/target, root vector, empty accepted states, open DAG, and artifact inventory agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0343/IntakeProbe.lean)` | exit 0; all four pinned Poisson-summation declarations elaborated under Lean 4.29.0 |
| `git diff --check -- Stage1_Instances/THM-M-0343` | exit 0; no output |

Known downstream failures are intentionally open: pinpoint human source and review; exact statement
selection, expression fingerprint, checked transports, and mutations; discovery and obligation
freezes; anchor/provenance/trust audit; proof and composition; hermetic replay; independent review;
and release acceptance. These prevent theorem completion but do not invalidate a truthful planned
intake.
