import Mathlib.Analysis.InnerProductSpace.LaxMilgram

/-!
# THM-M-0329 immutable mathlib anchor

This is a narrow candidate adapter for the anchor-audit phase. It checks that
the pinned mathlib continuous equivalence implies the already frozen target;
acceptance as the theorem proof remains a later workflow decision.
-/

noncomputable section

namespace Stage1Instances.THM_M_0329.AnchorAudit

open InnerProductSpace

universe u

def LaxMilgramTarget : Prop :=
  forall (V : Type u) [NormedAddCommGroup V] [InnerProductSpace Real V]
    [CompleteSpace V] (B : V →L[Real] V →L[Real] Real),
      IsCoercive B ->
        forall F : V →L[Real] Real,
          ∃! u : V, forall v : V, B u v = F v

/-- Exact adapter from pinned mathlib's Lax-Milgram equivalence to the frozen
existence-and-uniqueness target. -/
theorem canonicalTarget_mathlib_candidate :
    LaxMilgramTarget.{u} := by
  intro V _ _ _ B hB F
  let e := hB.continuousLinearEquivOfBilin
  let f := (toDual Real V).symm F
  refine ⟨e.symm f, ?_, ?_⟩
  · intro v
    rw [← hB.continuousLinearEquivOfBilin_apply]
    simp [e, f]
  · intro y hy
    apply e.injective
    apply ext_inner_right Real
    intro v
    rw [hB.continuousLinearEquivOfBilin_apply, hy v]
    simp [e, f]

end Stage1Instances.THM_M_0329.AnchorAudit

#print axioms Stage1Instances.THM_M_0329.AnchorAudit.canonicalTarget_mathlib_candidate
