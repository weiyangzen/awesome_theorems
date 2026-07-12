# Intake validation

Base revision: `84447940cf503cb83cb4fd16670216427c19bf18`.

Validation is intentionally limited to manifest consistency, dossier structure, JSON syntax, the
available pinned Lean executable, prohibited-token scanning, and whitespace. No canonical Lean
expression has been selected, so no elaboration or kernel-proof result is claimed. No `.lake`
content was fetched or mutated; the automation-provided untracked `Formalizations/Lean/.lake`
symlink reuses the canonical pinned artifacts and makes this a nonrelease dirty-tree run.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1120` | 0 | rank 560; planned; L0/rework_required; hard-mathlib-anchor-and-wrapper lane; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, x86_64 Linux, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `python3 -m json.tool Stage1_Instances/THM-M-1120/intake.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-1120/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python assertions over both JSON files and the six-file dossier | 0 | `intake invariant check: ok`; identity/rank/lifecycle/vector/open target and downstream DAG agree |
| `rg -n '(^|[[:space:]])(sorry\|admit)([[:space:]]\|$)\|^[[:space:]]*(axiom\|unsafe)[[:space:]]' Stage1_Instances/THM-M-1120` | 1 | expected no-match result; no prohibited proof device occurs in the dossier |
| `git diff --check -- Stage1_Instances/THM-M-1120 .stage1-worker-selftest.json` | 0 | no output; no scoped whitespace errors |

Known downstream failures are immutable primary-source selection and independent review, exact
Lean elaboration and mutation tests, formal-anchor audit, obligation registry, proof, hermetic
replay, independent validation, and master acceptance. They prevent theorem completion but do not
invalidate this self-tested fail-closed intake.
