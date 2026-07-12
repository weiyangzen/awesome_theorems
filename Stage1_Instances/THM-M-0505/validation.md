# Intake validation record

Base revision: `3f994388953e417edafd54b069ab45d648619698`.

Validation is scoped to manifest membership, planned-dossier invariants, JSON
syntax, a narrow pinned Lean API probe, forbidden proof escapes, and whitespace.
It does not test or claim an exact Weil formula or proof. The canonical pinned
`.lake` artifacts were reused read-only; no dependency update or fetch ran.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0505` | 0 | rank 879; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0505/instance.json >/dev/null` | 0 | valid JSON |
| `python3 -m json.tool Stage1_Instances/THM-M-0505/task-dag.json >/dev/null` | 0 | valid JSON |
| scoped Python intake assertions | 0 | `intake invariant check: ok`; IDs, rank, lifecycle, exact file inventory, empty accepted states, null formal expression/hash, incomplete terminal states, and six open downstream tasks agree |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0505/IntakeProbe.lean)` | 0 | Lean 4.29.0 elaborated `riemannZeta`, `ArithmeticFunction.vonMangoldt`, `Real.fourierIntegral`, `intervalIntegral`, `Complex.Gamma`, and `Summable` from pinned mathlib |
| `rg -n '\b(sorry\|axiom)\b' Stage1_Instances/THM-M-0505 --glob '!validation.md'; test $? -eq 1` | 0 | no forbidden-token match; `rg` returned its expected no-match status 1 |
| `git diff --check -- Stage1_Instances/THM-M-0505` | 0 | no whitespace errors |

Known downstream failures are deliberate and fail closed: immutable source and
errata review, exact equation and expression hash, mutation tests, formal-anchor
audit, frozen obligation/discovery registries, proof, source/readability review,
hermetic replay, independent validation, and master acceptance remain open.
