# Statement validation record

Item: `S56-M-0983-STATEMENT`  
Base revision: `32f565ebdf8b093386e287c150f0a2c7292903dc`

## Frozen target

`Stage1Instances.THM_M_0983.BernoulliStrongLawTarget` formalizes the intake-selected strong-law
reading. The probability space, real-valued observations, integrability, family-level joint
independence, identical distributions, almost-everywhere `0/1` values, and expectation-to-success-
probability equation are explicit. Its conclusion is almost-sure convergence of the empirical
frequency to `p`. The sole direct import is `Mathlib.Probability.StrongLaw`.

`target_iff_expandedIntakeShape` kernel-checks the direct expansion. This phase deliberately does
not import the historical `S1_M_263` module, credit its wrapper proof, or substitute the weaker
convergence-in-probability reading.

## Commands and results

All Lean commands ran from `Formalizations/Lean` using the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0983/Statement.lean` | 0 | exact target, expanded-intake iff, four mutations, and the empty-average boundary elaborated; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0983/check_statement.py` | 0 | expression SHA-256 `4ede545e65b98238682074217b653440c28d5e840f9ef21e74180a862d473845`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum ../../Stage1_Instances/THM-M-0983/Statement.lean lean-toolchain lake-manifest.json` | 0 | hashes recorded in `statement.json` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | repository standard and 1546-target projection valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0983` | 0 | rank 263, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-0983/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0983` | 0 | no whitespace errors |

## Mutation and status boundary

The validator compares explicit elaborated expressions and distinguishes removal of independence,
changing the observation codomain from `Real` to `Nat`, existentially rebinding `p`, and removing
the probability-measure hypothesis. `empiricalFrequency_zero` checks the chosen `n = 0` convention.
The endpoint probabilities `p = 0` and `p = 1` remain in scope.

This is self-tested statement evidence pending master acceptance. Source pinning, anchor audit,
proof, trust closure, and independent validation remain downstream, so no theorem completion is
claimed.
