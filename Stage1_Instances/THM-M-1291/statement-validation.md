# Statement validation

Base revision: `8f4c72eeb09c3eab9ea2ef5a83d0bf48d59fdce6`.

Commands ran from the repository root on 2026-07-12 unless the command
explicitly changes directory.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1291/Statement.lean` | 0 | Lean elaborated the canonical target, checked definitional transport, mutations, and final explicit `#print` |
| `python3 Stage1_Instances/THM-M-1291/check_statement.py` | 0 | expression SHA-256 `d33af3afa4d754bac48547f753d7bda319f46e538766e7c763fa437376599884`; all four structural mutations distinguished |
| `python3 -m json.tool Stage1_Instances/THM-M-1291/statement.json` | 0 | valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1291` | 0 | rank 462, planned, L0/rework_required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1291` | 0 | no whitespace errors |

The pinned environment was Lean 4.29.0 commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740` and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The direct import is only
`Mathlib.MeasureTheory.Integral.Bochner.Basic`; it supplies the measure,
Bochner-integral, filter, complex-norm, and `Real.rpow` vocabulary required by
the target.

This is statement-node evidence only. No proof of the Brezis-Lieb lemma and no
theorem-completion evidence is claimed.
