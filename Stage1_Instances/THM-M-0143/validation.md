# Intake validation

Base revision: `fe07aee0ce546497b6b69c8f7dcf910f374c09b1`.

Commands were run from the worker clone root on 2026-07-12. Exact results are recorded after the
final dossier-local checks. These are structural intake checks, not Lean kernel validation; there
is no exact Lean target at this phase.

| Command | Exit | Result |
|---|---:|---|
| `python3 -m json.tool Stage1_Instances/THM-M-0143/intake.json >/dev/null` | 0 | Structured intake parsed successfully |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0143` | 0 | Rank 318; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0143` | 0 | No whitespace errors |
| `rg -n '\\b(sorry\|axiom)\\b' Stage1_Instances/THM-M-0143` | 1 | No forbidden proof constructs found; exit 1 means no matches |

This intake is self-tested as a truthful planned dossier. Statement identification, all Lean proof
and validation work, master acceptance, and theorem completion remain open.
