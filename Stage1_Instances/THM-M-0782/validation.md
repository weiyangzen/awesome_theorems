# Intake validation

Base revision: `444819795285695894ff7b29af5c2419e0e000fa`.

The worker clone begins with an untracked `Formalizations/Lean/.lake` link to canonical pinned
artifacts. This task did not create or mutate it. The checks below are scoped intake evidence, not
clean release evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-0782` | 0 | rank 787; planned; hard-statement-first lane; theorem completion false |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-0782/intake.json >/dev/null` | 0 | intake artifact is valid JSON |
| dossier identity/reference self-check recorded below | 0 | exact item identity, planned/open status, and public merge targets validated |
| forbidden proof-placeholder scan recorded below | 0 | no Lean proof placeholder or accepted proof state appears in the dossier |
| `git diff --check -- Stage1_Instances/THM-M-0782 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The dossier self-check parses `intake.json`, checks the theorem ID, item ID, rank, and lifecycle,
requires null canonical/formal statements and an empty accepted-proof list, rejects theorem/audit
completion, and verifies both public merge targets exist. The placeholder scan checks the owned
files for the Lean proof tokens `sorry`, `admit`, and `sorryAx`.

No Lean theorem was elaborated because the exact mathematical root is deliberately unresolved.
The Lean version command checks availability of the pinned toolchain only and is not statement or
proof evidence. The first remaining gate is source-level selection of the exact Martin-Steel claim,
after master acceptance of this intake.
