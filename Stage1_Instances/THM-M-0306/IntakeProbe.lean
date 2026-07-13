import Mathlib.Analysis.FunctionalSpaces.SobolevInequality

/-!
# THM-M-0306 discovery-only intake probe

These checks authenticate pinned `L^p`, Frechet-derivative, compact-support, and
Gagliardo-Nirenberg-Sobolev interfaces adjacent to a future source-selected Friedrichs inequality.
They do not select the catalogue's exact statement, define a Sobolev-space root, establish a
support-to-zero-trace transport, or prove THM-M-0306.
-/

open MeasureTheory

#check eLpNorm
#check fderiv
#check HasCompactSupport
#check eLpNorm_le_eLpNorm_fderiv_one
#check eLpNorm_le_eLpNorm_fderiv_of_eq
#check eLpNorm_le_eLpNorm_fderiv_of_le
#check eLpNorm_le_eLpNorm_fderiv
