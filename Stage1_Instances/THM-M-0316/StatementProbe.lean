import Mathlib.Analysis.Normed.Operator.FredholmAlternative

/-!
Pinned-environment substrate probe for the THM-M-0316 exact-statement blocker.

These checks establish that mathlib exposes the nonzero-spectrum and Fredholm-alternative
components mentioned by the intake. They do not select those components as the canonical
Riesz-Schauder target and receive no statement or proof credit.
-/

#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet

