# Statement validation record

Item: `S56-M-1184-STATEMENT`  
Base revision: `e0fbcaa7059e060c07df329438cbec38eba068d4`

## Frozen target

`Stage1Instances.THM_M_1184.KantorovichDualityTarget` is the exact intake-selected compact-metric,
continuous real-cost claim. Couplings are probability measures on the product with both marginal
equalities. Dual pairs are signed continuous real potentials with the pointwise sum constraint.
The conclusion is equality of the real `sInf` of primal integrals and real `sSup` of dual
objectives. The module uses only the pinned probability-measure and Bochner-integral imports.

The historical `CompactMetricStatementShape` has incompatible cost and potential codomains and an
auxiliary data-package conclusion, so no fake definitional transport is asserted.

## Commands and results

Commands ran in this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1184/Statement.lean` | 0 | Exact target, four mutations, and zero-cost signed-potential boundary elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1184/check_statement.py` | 0 | Expression SHA-256 `edb496...1cc29`; statement SHA-256 `e9f16c...fbb2`; all four mutations distinguished |
| `printf 'import Mathlib.MeasureTheory.Integral.Bochner.Basic\n#check ProbabilityMeasure\n' \| lake env lean /dev/stdin` | 1 | Expected minimal-import negative probe: `ProbabilityMeasure` is unknown without its direct import |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard valid: 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ranks; all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1184` | 0 | Rank 169, planned, theorem incomplete |

The negative import probe is intentional evidence rather than a known failure. No `.lake` content
was fetched or updated. This node is statement-only evidence pending master acceptance and does not
claim a proof, theorem completion, or any dependent-node progress.
