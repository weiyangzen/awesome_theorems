/-
This probe checks the closest pinned mathlib statement discovered for Cauchy's
derivative estimate. It is not the canonical THM-M-1145 target: the repository
source does not identify one exact member of the theorem family.
-/
import Mathlib.Analysis.Complex.Liouville

#check Complex.norm_iteratedDeriv_le_of_forall_mem_sphere_norm_le
#check Complex.norm_deriv_le_of_forall_mem_sphere_norm_le
