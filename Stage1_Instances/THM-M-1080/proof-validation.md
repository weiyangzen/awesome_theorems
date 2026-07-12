# THM-M-1080 proof-phase validation

Item: `S56-M-1080-PROOF`

## Result

Verdict: `blocked` (partial kernel-checked progress, no proof-phase completion claim).

`Proof.lean` supplies real proof bodies for the frozen telescoping obligation, the `t = 0`
boundary, and final recomposition conditional only on the positive-threshold package. The exact
root remains open because the positive-threshold package has not been derived.

## First blocker

The pinned mathlib theorem
`ProbabilityTheory.measure_sum_ge_le_of_hasCondSubgaussianMGF` requires a
`StandardBorelSpace` instance and per-increment `HasCondSubgaussianMGF` hypotheses. The frozen
target quantifies over an arbitrary measurable space and supplies only `Martingale` plus almost
sure absolute increment bounds. No pinned theorem converts those exact premises to the required
conditional sub-Gaussian hypotheses. Importing the candidate would therefore strengthen the target.
Closing the phase requires a new arbitrary-space conditional Hoeffding lemma and its integrability,
conditional-expectation, and finite-iteration proof bodies.

## Validation evidence

Base revision: `23465358b632677fd22bc17941cba30db19d8176`.

| Command | Exit | Exact result summary |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1080` | 0 | rank 522; planned; theorem_complete false |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1080/Proof.lean` | 0 | all three declarations elaborated; each axiom report contains exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `rg -n -i '\\b(sorry\|admit\|axiom)\\b' Stage1_Instances/THM-M-1080 --glob '*.lean'` | 1 | no matches |
| `git diff --check -- Stage1_Instances/THM-M-1080` | 0 | no output |

Because the required positive-threshold body and hence the assigned proof phase remain open, no
`.stage1-worker-selftest.json` is emitted.
