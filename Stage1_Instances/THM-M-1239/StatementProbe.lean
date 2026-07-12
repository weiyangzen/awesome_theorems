import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-1239 statement substrate probe

This file checks only the closest pinned mathlib substrate named by the source
gloss. It is not a canonical Poincare-inequality target: the repository does
not select a domain, Sobolev model, normalization, exponent, or constant.
-/

open MeasureTheory

#check eLpNorm
#check fderiv
#check eLpNorm_le_eLpNorm_fderiv_of_eq
#check eLpNorm_le_eLpNorm_fderiv_of_le

