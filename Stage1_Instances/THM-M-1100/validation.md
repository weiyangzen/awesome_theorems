# Intake validation

Base revision: `410d43b85faead588dace9d83e6bc4c4c7e0eaf1`.

Validation is limited to manifest consistency, dossier structure, scoped planned-intake
invariants, pinned-environment API availability, JSON syntax, and whitespace. The literal source
label is not a proposition, so the Lean file is explicitly an API probe rather than a canonical
target or proof. No statement-gate or kernel-proof result is claimed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1100` | exit 0; rank 540, L0/rework_required, planned, legacy artifacts unaccepted, theorem_complete false |
| `python3 -m json.tool Stage1_Instances/THM-M-1100/instance.json` and `task-dag.json` | exit 0; valid JSON |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1100/IntakeProbe.lean)` | exit 0; pinned Lean elaborated `Kernel`, `IsMarkovKernel`, and `Invariant` API checks |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| forbidden-token scan of `IntakeProbe.lean` | exit 1; no `sorry`, `axiom`, or `admit` token found |
| `git diff --check -- Stage1_Instances/THM-M-1100` | exit 0; no output |

The first downstream failed gate is statement identity: "MCMC methods" does not select a
proposition. Retry requires an authorized selection and independent inspection of one exact source
theorem, including all assumptions and the boundary against `THM-M-1101`. Canonical Lean
elaboration and mutation tests, formal-candidate audit, obligation registry, proof, hermetic replay,
and independent release validation remain open. These failures prevent audit and theorem
completion but do not invalidate this truthful planned intake.
