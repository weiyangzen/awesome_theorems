import Mathlib.Analysis.Subadditive
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.LinearAlgebra.Basis.Flag
import Mathlib.MeasureTheory.Function.L1Space.Integrable
import Mathlib.RingTheory.Grassmannian

/-!
# Pinned mathlib anchor audit for THM-M-1419

These checks authenticate nearby infrastructure in the pinned dependency closure.
None of the declarations below states or proves the Oseledets target.
-/

open MeasureTheory

#check Subadditive.tendsto_lim
#check MeasurePreserving.integrable_comp
#check Ergodic.ae_eq_const_of_ae_eq_comp_ae
#check Flag
#check Module.Basis.toFlag
#check Module.Grassmannian
#check Module.Grassmannian.toSubmodule
