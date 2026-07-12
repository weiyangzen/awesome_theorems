import Mathlib.Analysis.Normed.Operator.BanachSteinhaus

/-!
# THM-M-0312 pinned anchor checks

This file checks the exact mathlib wrapper and the two nearby public formulations at the pinned
revision. The checks establish candidate identity only; later gates own obligation composition,
release-grade trust closure, and theorem completion.
-/

namespace Stage1Instances.THM_M_0312.AnchorAudit

universe uE uF uK uK2 uI

variable {E : Type uE} {F : Type uF} {K : Type uK} {K2 : Type uK2}
  [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
  [NontriviallyNormedField K] [NontriviallyNormedField K2]
  [NormedSpace K E] [NormedSpace K2 F]
  {sigma12 : K →+* K2} [RingHomIsometric sigma12]
  {I : Type uI} [CompleteSpace E]

/-- A repo-local exact-type wrapper around the pinned mathlib proof body. -/
theorem exactMathlibWrapper {g : I → E →SL[sigma12] F}
    (h : forall x : E, exists C : Real, forall i : I, norm (g i x) <= C) :
    exists C' : Real, forall i : I, norm (g i) <= C' :=
  banach_steinhaus h

/-- The alternate extended-nonnegative-supremum formulation also resolves at the pin. -/
example {g : I → E →SL[sigma12] F}
    (h : forall x : E, (iSup fun i : I => (nnnorm (g i x) : ENNReal)) < ⊤) :
    (iSup fun i : I => (nnnorm (g i) : ENNReal)) < ⊤ :=
  banach_steinhaus_iSup_nnnorm h

#check WithSeminorms.banach_steinhaus
#check NormedSpace.equicontinuous_TFAE
#print axioms exactMathlibWrapper
#print axioms banach_steinhaus
#print axioms banach_steinhaus_iSup_nnnorm
#print axioms WithSeminorms.banach_steinhaus

end Stage1Instances.THM_M_0312.AnchorAudit
