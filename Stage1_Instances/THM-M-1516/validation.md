# Intake validation

Base revision: `61369637c5db864082a624c34c62a91e6741f9da`.

The preflight commands completed with exit code 0:

- `python3 Docs/tools/check_stage1_standard.py` -> `ok` with 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill present.
- `python3 scripts/stage1_target.py check` -> `ok` with 1546 unique targets and ranks 1..1546.
- `python3 scripts/stage1_target.py show THM-M-1516` -> rank 185, `planned`, `L0`, `rework_required: true`, theorem incomplete.

The dossier-local checks below were run after creation. They validate JSON syntax, required identity
fields, forbidden-token absence, and whitespace only. No Lean command is claimed: intake truthfully
stops before an exact Lean proposition can be selected.

- `jq -e '.schema_version == "stage1-instance/5.6.0" and .item_id == "S56-M-1516-INTAKE" and .theorem_id == "THM-M-1516" and .lifecycle_mode == "planned" and .theorem_complete == false' Stage1_Instances/THM-M-1516/intake.json` -> exit 0, output `true`.
- A forbidden-proof-token scan over `intake.json`, `README.md`, and `source_statement_crosswalk.md` -> exit 0, no matches.
- `git diff --check -- Stage1_Instances/THM-M-1516` -> exit 0, no output.
