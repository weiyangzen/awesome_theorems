import Mathlib.Combinatorics.Additive.Corner.Roth
import Mathlib.NumberTheory.DiophantineApproximation.Basic
import Mathlib.NumberTheory.Height.Basic
import Mathlib.NumberTheory.SiegelsLemma
import Mathlib.NumberTheory.Transcendental.Liouville.LiouvilleWith

/-!
# Checked anchors for THM-M-0398

This module checks the declarations found by the pinned-source audit. None of
them has the type of the canonical Thue-Siegel-Roth target in `Statement.lean`.
-/

#check Real.infinite_rat_abs_sub_lt_one_div_den_sq_of_irrational
#check Rat.finite_rat_abs_sub_lt_one_div_den_sq
#check Real.infinite_rat_abs_sub_lt_one_div_den_sq_iff_irrational
#check LiouvilleWith
#check LiouvilleWith.exists_pos
#check Height.mulHeight₁
#check Height.logHeight₁
#check roth_3ap_theorem
#check roth_3ap_theorem_nat
