# Statement validation record

Item: `S56-M-1148-STATEMENT`  
Base revision: `3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`

## Frozen target

`Stage1Instances.THM_M_1148.PoissonIntegralFormula` is the exact disk Dirichlet claim selected by
the intake. For `0 < R` and real data continuous on `sphere c R`, it asks for a function harmonic
on `ball c R`, continuous on `closedBall c R`, equal to the data on the sphere, and represented at
each interior point by `Real.circleAverage (poissonKernel c w • g) c R`.

The single direct import is `Mathlib.Analysis.Complex.Harmonic.Poisson`. This phase fixes and
elaborates a proposition only. It does not use the nearby harmonic-function representation theorem
as proof of existence from arbitrary boundary data.

## Commands and results

All commands ran inside the worker clone. Lean used the existing pinned Lake closure; no dependency
update, build, clone, or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1148/Statement.lean` | 0 | canonical target and five mutation fixtures elaborated; explicit expression printed |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-1148/check_statement.py` | 0 | expression SHA-256 `4631cdf8cf607ec85b6c0e053d81966f967247daf9952a6edcbdfee6ac4016d8`; all five mutations distinguished; source SHA-256 `7e17ed32e812a1b846ff168947684ac8930bbffe3c0f410ea4bea558c22ad25d` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |

The mutations remove positive radius, change the codomain, change binder/premise scope, extend the
formula to the closed disk, and remove the boundary trace. Distinct expression fingerprints show
that none aliases the root. Primary-source pinpoint review, anchor/body audit, proof, hermetic
replay, and independent review remain open. No theorem-completion claim is made.
