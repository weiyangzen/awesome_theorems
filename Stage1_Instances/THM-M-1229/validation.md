# Intake validation

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

The following checks were run from the repository root. Their scope is the
intake dossier only; no Lean theorem or source-fidelity gate is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1229` | 0 | rank 157, lane `hard_mathlib_anchor_and_wrapper`, lifecycle `planned`, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1229/intake.json` | 0 | valid JSON |
| dossier-local reference and boundary check (recorded in worker self-test) | 0 | required files and conservative status markers found |
| `git diff --check -- Stage1_Instances/THM-M-1229` | 0 | no whitespace errors |

Known open gates: exact primary-source pinpoint and errata audit, canonical Lean
statement elaboration, expression and environment fingerprints, transport and
mutation tests, obligation registry, proof, trust/provenance, and release
validation.
