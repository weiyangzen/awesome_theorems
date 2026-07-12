# Intake validation

Base revision: `c8bb1d8f046a4b2816eb059edc201b88d2063f42`.

Validation is limited to manifest consistency, dossier structure, pinned source discovery, scoped
intake invariants, and whitespace. The existing untracked `Formalizations/Lean/.lake` link/artifact
predates this work and is preserved as unrelated dirty-tree state. No canonical Lean expression has
been selected, so this intake makes no kernel-proof claim and does not mutate `.lake`.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0156` | exit 0; rank 655, L0/rework_required, planned, theorem_complete false |
| `rg -n "theorem integral_divergence_of_hasFDerivAt_off_countable|theorem integral_divergence_prod_Icc_of_hasFDerivAt_of_le|theorem integral2_divergence_prod_of_hasFDerivAt" Formalizations/Lean/.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/DivergenceTheorem.lean` | exit 0; all three named pinned declarations found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0156/IntakeProbe.lean` | exit 0; Lean elaborated all three pinned candidate declarations |
| `python3 -m json.tool Stage1_Instances/THM-M-0156/instance.json` | exit 0 |
| `python3 -m json.tool Stage1_Instances/THM-M-0156/task-dag.json` | exit 0 |
| scoped Python intake assertions | exit 0; `intake invariant check: ok` |
| `git diff --check -- Stage1_Instances/THM-M-0156` | exit 0; no output |

Known downstream failures are deliberately open: pinpoint human-source inspection and independent
review; exact domain, boundary, and regularity choices; canonical Lean elaboration; candidate
provenance/axiom audit; obligation expansion; proof composition; hermetic replay; and independent
verification. They prevent audit and theorem completion but do not invalidate this fail-closed
`planned` intake.
