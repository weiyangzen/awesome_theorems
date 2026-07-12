import Mathlib.Analysis.Calculus.ContDiff.Basic
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.LinearAlgebra.BilinearMap

/-!
# THM-M-1553 anchor probes

These checks establish the APIs available in the pinned mathlib snapshot. They
are infrastructure probes only, not a proof of `HirotaKdVTarget`.
-/

#check ContDiff
#check ContDiff.differentiable
#check deriv
#check deriv_add
#check deriv_mul
#check deriv_comp
#check Real.hasDerivAt_log
#check iteratedDeriv
#check LinearMap.BilinMap
#check LinearMap.map_add₂
#check LinearMap.map_smul₂

