# THM-M-1009 proof-phase attempt

Item: `S56-M-1009-PROOF`  
Base revision: `11ec0ea4b441f1e6bc5580ca9a037509892e8c92`  
Attempt date: 2026-07-12

## Implemented proof bodies

`Proof.lean` provides checked local bodies for the following frozen proof
architecture inputs:

- nonnegativity of the numerator, denominator, and finite ratio;
- positivity of the ordered double-intersection denominator when the single
  probability sum is positive;
- measurability, integrability, and pointwise nonnegativity of the finite event
  count;
- the first-moment identity between the event-count integral and
  `partialEventMass`;
- the pointwise square expansion and second-moment identity between the
  squared event-count integral and `pairwiseEventMass`.

All declarations are proof-bearing and use only the pinned mathlib import.
The four representative axiom reports contain only mathlib's ordinary
foundation profile: `propext`, `Classical.choice`, and `Quot.sound`.

## Honest completion boundary

This attempt does not close `ErdosRenyiLowerBoundTarget`. The remaining root
cut set is:

1. the finite Cauchy-Schwarz lower bound relating the positive support of the
   event count to its first and second moments;
2. the shifted-window comparison that turns the finite lower bound into the
   frozen initial-segment `Filter.limsup` ratio under divergence;
3. continuity from above for the measurable tail unions and their exact
   identification with `limsup A atTop`;
4. unconditional assembly of these results into the canonical root.

The second item is the first failed gate. Neither pinned mathlib nor the
audited local sources expose that exact analytic bridge, and implementing it
was not completed in this execution. Consequently this proof node is blocked,
the root remains open, and no worker self-test manifest is emitted.

## Validation record

Working directory for the Lean commands was `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1009/Proof.lean` | 0 | all local proof bodies elaborate; representative axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 targets validate |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1009` | 0 | rank 289, planned, theorem incomplete |
| `rg -n '\b(sorry\|admit)\b\|(^\|[^A-Za-z])axiom[[:space:]]+[A-Za-z_]' Stage1_Instances/THM-M-1009/Proof.lean` | 1 | no placeholder terms or axiom declarations in the proof source; exit 1 means no matches |
| `git diff --check -- Stage1_Instances/THM-M-1009` | 0 | no whitespace errors |

No dependency update, build, clone, or fetch command was run.
