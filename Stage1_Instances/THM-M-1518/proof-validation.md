# THM-M-1518 proof attempt

Item: `S56-M-1518-PROOF`  
Date: `2026-07-12`  
Base revision: `6799b5daa49cdaafb2a4d4eab837b06d9f795666`

## Verdict

`blocked`: the exact theorem has no eligible proof body in the repository or
the pinned mathlib closure. `ObligationTree.exactTarget_of_packages` is a real
kernel-checked composition theorem, but it requires inhabitants of
`FirstVariationFormula` and `WeakToPointwise`. Neither inhabitant exists. The
frozen minimum root cut set is `M1518-N-DIFFERENTIATE`, `M1518-L-IBP`, and
`M1518-L-FUNDAMENTAL`.

Closing those nodes requires substantial new variational-analysis
formalization: differentiation of the parameterized interval action,
fixed-endpoint integration by parts for the momentum term, and a fundamental
lemma plus continuity upgrade producing the pointwise `HasDerivAt` conclusion.
Pinned mathlib contains prerequisite APIs but no terminal declaration. The
audited Physlib declarations are nonterminal, use different pins, and are not
in this repository's dependency closure. The historical `S1_M_187` proves the
opposite implication and cannot be substituted.

No proof source, axiom, placeholder, unsafe declaration, weakened statement,
or unpinned dependency was added. Because the assigned proof phase is not
self-tested complete, this attempt deliberately does not create
`.stage1-worker-selftest.json`.

## Narrow validation evidence

All commands ran from the worker clone on `2026-07-12`. The pre-existing
`Formalizations/Lean/.lake` symlink points at the canonical pinned artifacts;
it was reused but not modified. No update, build, clone, fetch, or dependency
mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard passes: 15 assurance groups and 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passes: 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1518` | 0 | Rank 187, planned, hard-mathlib-anchor lane, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1518/check_obligation_tree.py` | 0 | Statement and conditional composition elaborate with `lake env lean`; 12 obligations and 26 typed edges pass; root remains open at M4. |
| `rg -n -i 'StationaryActionEulerLagrangeTarget\|FirstVariationFormula\|WeakToPointwise\|stationary action\|least action\|Euler[-_ ]?Lagrange\|fundamental theorem of variational' --glob '*.lean' Stage1_Instances/THM-M-1518 Formalizations/Lean/AwesomeTheorems Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | Hits contain this conditional dossier, historical metadata/wrappers, and prerequisite APIs; no exact terminal proof body was found. |
| `rg -n '^\\s*(sorry\|admit\|axiom)(\\s\|$)\|sorryAx\|unsafe' Stage1_Instances/THM-M-1518 -g '*.lean'` | 1 | No prohibited Lean declaration token found; exit 1 means no match. |

The obligation-tree Lean run reports that
`exactTarget_of_packages` depends only on `propext`, `Classical.choice`, and
`Quot.sound`. That establishes conditional composition only; it does not
inhabit either open analytic package or close the canonical root.
