# Intake validation record

Base revision: `b7e3d69a2e15f24ccd7e02f04ae9e5a1a31e52fe`.

This record is completed after running the commands below. It is an intake-only evidence surface:
no Lean declaration or proof was introduced, so toolchain availability is not kernel evidence for
the generalized Stokes theorem.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard structure passes: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest passes: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0154` | 0 | rank 653; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | pinned toolchain is available; no dependency mutation or build was performed |
| `python3 -m json.tool Stage1_Instances/THM-M-0154/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `test "$(find Stage1_Instances/THM-M-0154 -maxdepth 1 -type f \| wc -l)" -eq 4` | 0 | exactly the four intended intake artifacts exist |
| `rg -n '(^\|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*axiom[[:space:]]' Stage1_Instances/THM-M-0154` | 1 | no Lean proof escape or axiom declaration found; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-0154 .stage1-worker-selftest.json` | 0 | no whitespace errors before self-test emission |

Master acceptance, exact-statement elaboration, source audit, proof, kernel validation, and release
remain outstanding.
