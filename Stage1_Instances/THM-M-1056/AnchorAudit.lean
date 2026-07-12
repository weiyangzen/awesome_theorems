import Mathlib.Analysis.Subadditive
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.Dynamics.Ergodic.MeasurePreserving
import Mathlib.LinearAlgebra.Basis.Flag
import Mathlib.MeasureTheory.Function.L1Space.Integrable
import Mathlib.RingTheory.Grassmannian

/-!
# THM-M-1056 anchor audit

This file checks only the nearby declarations available in the repository's
pinned mathlib. None of them states Oseledets' multiplicative ergodic theorem.
-/

#check Subadditive.tendsto_lim
#check MeasureTheory.MeasurePreserving.iterate
#check MeasureTheory.MeasurePreserving.integrable_comp
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#check Flag
#check Module.Basis.flag
#check Module.Grassmannian
#check Module.Grassmannian.toSubmodule
