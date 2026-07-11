# Statement validation record

Item: `S56-M-0424-STATEMENT`  
Base revision: `e057ea3c85e142707a88ea3fc13445bebddca902`

## Frozen target

`Stage1Instances.THM_M_0424.BrauerGroupStatement` quantifies over every field `K` and asks for
the complete bundled construction: tensor-product representatives and congruence, base-field
identity, opposite-algebra inverses, and one linked `CommGroup (BrauerGroup K)` instance. This is
the full intake-selected field-level group statement, not the weaker quotient-equality wrapper.

The two direct imports are minimal for this expression. `Mathlib.Algebra.BrauerGroup.Defs` supplies
the CSA quotient model; removing `Mathlib.RingTheory.TensorProduct.Basic` produced a real elaboration
failure at `tensorRep_equiv` because Lean could not synthesize the tensor-product semiring structure.

## Commands and results

Commands ran in this worker clone. Lean ran from `Formalizations/Lean` using the existing pinned
Lake environment. No dependency update, fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard consistent: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0424` | 0 | rank 78, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0424/Statement.lean` | 0 | exact target and all structural mutation expressions elaborated; explicit canonical expression printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0424/check_statement.py` | 0 | expression SHA-256 `62cfee70...3aa8`; all four structural mutations distinguished; pinned mathlib revision confirmed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 -m json.tool Stage1_Instances/THM-M-0424/statement.json >/dev/null` | 0 | structured statement record is valid JSON |
| `rg -n '\b(sorry\|axiom\|admit)\b' Stage1_Instances/THM-M-0424/Statement.lean Stage1_Instances/THM-M-0424/check_statement.py` | 1 (expected) | no prohibited placeholders or axioms |
| `git diff --check -- Stage1_Instances/THM-M-0424 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is statement-only kernel evidence pending master acceptance. The module deliberately creates
no inhabitant of `BrauerGroupLawData`, so it supplies no proof evidence. Source acceptance, anchor
audit, obligation tree, proof, hermetic validation, independent verification, and release remain
open. The existing untracked `.lake` link was present at preflight and was used read-only.
