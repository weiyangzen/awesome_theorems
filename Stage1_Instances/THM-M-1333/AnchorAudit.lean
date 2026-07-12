import Mathlib.Analysis.ODE.PicardLindelof

/-!
# THM-M-1333 anchor audit probes

This file checks the nearest pinned mathlib declarations. They prove
Picard-Lindelof under a spatial Lipschitz hypothesis; they are deliberately
not wrappers for the continuity-only Peano target.
-/

#check IsPicardLindelof
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#check IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt₀
#check IsPicardLindelof.exists_forall_mem_closedBall_eq_forall_mem_Icc_hasDerivWithinAt

#print axioms IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt
#print axioms IsPicardLindelof.exists_eq_forall_mem_Icc_hasDerivWithinAt₀

namespace Stage1Instances.THM_M_1333.AnchorAudit

open Metric Set

/-- A checked probe making the extra spatial Lipschitz premise of the nearest
mathlib candidate explicit. This premise is absent from the Peano target. -/
theorem picardCandidateHasExtraLipschitz
    {E : Type*} [NormedAddCommGroup E] [NormedSpace Real E]
    {f : Real -> E -> E} {tmin tmax : Real} {t0 : Set.Icc tmin tmax}
    {x0 : E} {a r L K : NNReal}
    (h : IsPicardLindelof f t0 x0 a r L K) :
    ∀ t ∈ Set.Icc tmin tmax,
      LipschitzOnWith K (f t) (Metric.closedBall x0 a) :=
  h.lipschitzOnWith

end Stage1Instances.THM_M_1333.AnchorAudit
