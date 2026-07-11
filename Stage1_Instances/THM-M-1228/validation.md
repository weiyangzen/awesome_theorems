# Intake validation record

Base revision: `2b65f3efa70ae08a8776a86771b091957de1652e`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | rank 156, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/intake.json >/dev/null` | 0 | structured intake is valid JSON |
| `rg -n '\b(sorry\|axiom\|placeholder)\b' Stage1_Instances/THM-M-1228` | 1 | no forbidden proof-gap terms found (`rg` exit 1 means no matches) |
| `rg -n 'THM-M-1228\|S56-M-1228-INTAKE' Stage1_Instances/THM-M-1228` | 0 | dossier identifiers and local references are present |
| `git diff --check` | 0 | no whitespace errors |

This is an intake-only node: it introduces no Lean declaration and claims no
kernel validation, source acceptance, or theorem completion.

## Statement validation record

Item: `S56-M-1228-STATEMENT`. Base revision:
`4f4d4a793ede4c1ec0e5d2dd61add8a1fc35e616` (tree
`f1c2d8e703badfa50c715897da00a53feca91a38`).

Validation ran in the worker clone on 2026-07-12. The canonical pinned `.lake`
directory was reused through the pre-existing worker symlink. No update, build,
dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1228/Statement.lean` | 0 | Printed the elaborated target `CKNSourceSemantics -> Prop`; suitability implies zero parabolic measure of `SingularSet` |
| `python3 Stage1_Instances/THM-M-1228/check_statement.py` | 0 | expression SHA-256 `101ce8f2...8ecf58e5f`; four structural mutations distinguished; toolchain and mathlib pin matched |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1228` | 0 | rank 156, planned, legacy artifacts unaccepted, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1228/statement.json >/dev/null` | 0 | statement record is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1228 .stage1-worker-selftest.json` | 0 | no whitespace errors |

This evidence validates elaboration and statement mutation separation only.
`CKNSourceSemantics` is an explicit boundary for analytic notions missing from
the pinned library, not a postulated declaration or a proof package. Concrete
source-faithful definitions and transports remain obligations. There is no
CKN proof body, source acceptance, root closure, or theorem-completion claim.
