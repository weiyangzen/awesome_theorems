# THM-M-0995 proof execution report

Item: `S56-M-0995-PROOF`  
Base revision: `bafc08f4d75222633812affc69d9f5b903037bea`  
Verdict: blocked, with three proof packages kernel-checked

## Implemented bodies

`Proof.lean` implements the exact `ChernoffPackage`, `ZeroDenominatorPackage`, and
`AssemblyPackage` interfaces from the frozen obligation tree. The Chernoff body derives
integrability from the almost-sure summand bound before applying mathlib's pinned
`measure_ge_le_exp_mul_mgf`; it does not add an integrability assumption. The boundary body uses
the probability-measure bound, and the assembly body performs the denominator split and composes
the exact package interfaces.

All three declarations elaborate without an unproved proof primitive. Their reported axiom set is
exactly `propext`, `Classical.choice`, and `Quot.sound`.

## Fail-closed blocker

The frozen `OptimizeExponentPackage` is false. Its admissibility conclusion requires `s * b < 3`
for `s = t / (v + b*t/3)`. At the allowed values `v = 0`, `b = 1`, and `t = 1`, the denominator is
positive but `s * b = 3`. `Proof.not_optimizeExponentPackage` is a kernel-checked counterexample
to the package itself.

Consequently the proof phase cannot truthfully discharge the frozen root cut set. The obligation
tree must be repaired by splitting the zero-variance case (or by using non-strict admissibility
with a compatible MGF interface) before proof execution can close the root. The still-open
individual and sum MGF packages also require the planned Bernstein analytic development. No
worker self-test manifest is emitted because the assigned proof phase is not complete.

## Validation

Commands did not update, fetch, clone, or otherwise mutate the pinned dependency closure.

| Command | Exit | Result |
|---|---:|---|
| `cd Stage1_Instances/THM-M-0995 && LEAN_PATH=$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) -o Statement.olean Statement.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) -o ObligationTree.olean ObligationTree.lean && LEAN_PATH=.:$(cd ../../Formalizations/Lean && lake env printenv LEAN_PATH) $(cd ../../Formalizations/Lean && lake env which lean) Proof.lean` | 0 | all proof bodies and the optimizer counterexample elaborated; each axiom report omitted any unproved proof primitive |
| `rg -n 'sorryAx|\\bsorry\\b|\\badmit\\b' Stage1_Instances/THM-M-0995/Proof.lean` | 1 | no forbidden proof token (`rg` exit 1 means no match) |
| `git diff --check -- Stage1_Instances/THM-M-0995` | 0 | no whitespace errors |

This report claims only the three checked package bodies and the checked counterexample. It does
not claim root closure, proof-phase completion, theorem completion, validation, or release.
