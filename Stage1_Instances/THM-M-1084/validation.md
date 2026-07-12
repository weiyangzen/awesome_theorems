# Intake validation

Base revision: `128997c29e0211f5c45f2205b13ff707daad37d6`.

Validation is limited to manifest consistency, dossier structure, scoped intake invariants, JSON
syntax, and whitespace. There is no canonical Lean expression yet, so no elaboration or kernel
result is claimed.

| Command | Result |
|---|---|
| `python3 -m json.tool Stage1_Instances/THM-M-1084/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-1084/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1084` | exit 0; rank 526, L0/rework_required, planned, theorem_complete false |
| `git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json` | exit 0; no output |

Known downstream failures: exact primary-source inspection, canonical Lean elaboration and mutation
tests, formal-candidate audit, obligation registry, proof, hermetic replay, and independent review
remain open. They prevent theorem completion but do not invalidate this fail-closed planned intake.

Two development runs of the scoped assertion harness exited 1 because its test code first scanned
documentation for Lean-source tokens and then expected the theorem ID rather than the item-ID stem
inside task IDs. No dossier invariant failed. The final harness scans Lean files only (there are
none at intake), checks task IDs against `S56-M-1084`, and retains all structural assertions.

## Statement validation

Statement phase base revision: `7c40b39aac30d12a21a2ca13ebe9406d4d57b383`.

| Command | Result |
|---|---|
| `python3 Stage1_Instances/THM-M-1084/check_statement.py` | exit 0; expression SHA-256 `25bdfe85eaaa67694f865e6af60c240b013b2fbcd9acfb2949e5abdb0b34ca99`; all three structural mutations differ; singleton boundary proof elaborates |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1084/Statement.lean)` | exit 0; exact target and checked expansion elaborated with pinned artifacts; one harmless unused-variable linter warning in a mutation |
| `python3 -m json.tool Stage1_Instances/THM-M-1084/statement.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique ordered targets |
| `git diff --check -- Stage1_Instances/THM-M-1084 .stage1-worker-selftest.json` | exit 0; no output |

The statement validator compares Lean's elaborated `#print` expressions, not source text. It uses
the pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; no dependency was
updated or fetched. One development command used `../../../` rather than `../../` from
`Formalizations/Lean` and exited 1 with file-not-found. Another was mistakenly run from the
repository root and exited 1 because that directory is not the Lake workspace. Neither was an
elaboration failure; the commands recorded in the table use the correct working directory.

Known boundary: source audit has not yet established that this selected normalization is the exact
form of a pinpoint historical theorem. Anchor audit, obligation tree, proof, and every release gate
remain open. This phase claims only provisional exact Lean statement elaboration (`M3`), not a
proof, `H0`, audit completion, or theorem completion.
