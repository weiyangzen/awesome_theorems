# Intake validation record

Base revision: `ded29702119d0d4880db9fcf1d0a6560a89058fd`.

The worker tree already contained the unrelated untracked path `Formalizations/Lean/.lake`; it was
not modified or used as evidence. This intake adds no Lean source because the repository metadata
does not identify an exact proposition. Running `lake env lean` on an invented probe would not
validate the source statement, so no kernel elaboration result is claimed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0365` | 0 | rank 857, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0365/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test -f Stage1_Instances/THM-M-0365/README.md -a -f Stage1_Instances/THM-M-0365/source_statement_crosswalk.md -a -f Stage1_Instances/THM-M-0365/validation.md` | 0 | dossier, scope map, crosswalk, and validation record exist |
| `git diff --check -- Stage1_Instances/THM-M-0365 .stage1-worker-selftest.json` | 0 | no whitespace errors |

These checks establish target membership, repository-standard consistency, and the intake artifact
shape only. Master acceptance remains outstanding. Exact-statement elaboration, primary-source
audit, obligation freezing, proof, trust, reproducibility, and release gates remain open.
