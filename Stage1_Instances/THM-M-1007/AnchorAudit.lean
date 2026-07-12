import Mathlib.Probability.StrongLaw
import Mathlib.Probability.BorelCantelli
import Mathlib.Probability.Moments.Variance

/-!
# THM-M-1007 anchor probes

This file checks the types of the pinned mathlib declarations retained by the anchor audit.  They
are proof substrate only: none has the type of Kolmogorov's three-series biconditional.
-/

noncomputable section

open Filter MeasureTheory ProbabilityTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_1007.AnchorAudit

universe u

def truncationFunction (c : Real) (x : Real) : Real :=
  if ‖x‖ <= c then x else 0

theorem measurable_truncationFunction (c : Real) : Measurable (truncationFunction c) := by
  exact Measurable.ite (measurableSet_le measurable_norm measurable_const)
    measurable_id measurable_const

theorem independent_truncations
    {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    (X : Nat -> Omega -> Real) (hX : iIndepFun X mu) (c : Real) :
    iIndepFun (fun n omega => truncationFunction c (X n omega)) mu := by
  simpa [Function.comp_def] using
    hX.comp (fun _ : Nat => truncationFunction c)
      (fun _ : Nat => measurable_truncationFunction c)

#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun.comp
#check MeasureTheory.ae_eventually_notMem
#check ProbabilityTheory.IndepFun.variance_sum
#check ProbabilityTheory.variance
#check ProbabilityTheory.strong_law_ae

end Stage1Instances.THM_M_1007.AnchorAudit
