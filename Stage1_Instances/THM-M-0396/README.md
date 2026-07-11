# THM-M-0396: Baker's theorem

## Intake verdict

This is a rev-5.6 `planned` instance at `L0 / rework_required`. The repository
claim, "a lower bound for linear forms in logarithms", identifies a theorem
family, not a unique quantitative statement. The coefficient field, logarithm
branches, algebraicity and nonzero hypotheses, height convention, degree and
coefficient parameters, and explicit constant are not specified. They remain
open for the statement phase. No H0, M0, R0, Lean closure, or theorem completion
is claimed.

## Scope map

| Surface | Included | Excluded or unresolved |
|---|---|---|
| Mathematical object | A nonzero linear form in chosen logarithms of algebraic numbers | Baker-method applications and finite searches, owned by THM-M-0397 |
| Result | An effective positive lower bound in explicitly selected arithmetic parameters | A vague existence claim or an unrecorded choice among Baker, Baker-Wuestholz, and Matveev variants |
| Inputs | Future exact algebraic-number domain, logarithm choices, integer/algebraic coefficients, heights, and degree | Unrestricted complex inputs and zero linear forms |
| Formal surface | Lean 4 with pinned mathlib | Legacy status or declarations receiving proof credit automatically |
| Current phase | Dossier, scope boundary, source crosswalk, open task DAG | Exact statement, anchor acceptance, proof, validation, and release |

## Open task DAG

`STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
The statement phase must resolve `SRC-GAP-1` in the crosswalk before it can claim
an exact canonical proposition.

## Status boundary

The legacy file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_009.lean` is a
discovery hint only. Its abstract lower-bound data and local bridges neither
select the source theorem nor provide the missing analytic proof. Intake
validation checks only this planned record; it is not kernel evidence.
