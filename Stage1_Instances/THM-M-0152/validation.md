# Intake validation record

Base revision: `63728668acb87acd4bab7e755151dce89dc1eeb4`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0152` | 0 | rank 651, planned, L0/rework-required, no accepted legacy artifacts, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, release build |
| `rg -n -i 'gaussian curvature\|Gauss curvature\|Theorema\|sectionalCurvature\|sectional curvature\|local isometr' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Matches were unrelated uses of "theorem" and a Prime Number Theorem note; no relevant geometry declaration was found |
| `python3 -m json.tool` on `instance.json` and `task-dag.json` | 0 | Both structured intake artifacts parse as JSON |
| dossier file-presence assertion | 0 | `README.md`, `scope-map.md`, `source-statement-crosswalk.md`, `instance.json`, and `task-dag.json` exist and are nonempty |
| forbidden Lean escape-marker scan over the owned path | 0 | No forbidden proof escape marker occurs |
| `git diff --check -- Stage1_Instances/THM-M-0152 .stage1-worker-selftest.json` | 0 | No whitespace errors |

The existing `.lake` link in this worker clone points at canonical pinned artifacts and was not
modified. No dependency update, build, fetch, or clone was run. The Lean command validates the
pinned executable only: intake introduces no Lean declaration, so no kernel theorem result is
claimed.

