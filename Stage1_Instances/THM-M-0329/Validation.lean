import Statement
import Mathlib.Analysis.InnerProductSpace.LaxMilgram

/-!
# THM-M-0329 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact frozen target directly from the pinned Riesz and
Lax-Milgram equivalences. This is differential evidence within one worker,
not the distinct-runner verification required for release.
-/

noncomputable section

namespace Stage1Instances.THM_M_0329.Validation

open InnerProductSpace

universe u

/-- Direct, separately written reconstruction of the exact frozen target. -/
theorem laxMilgramDirect : LaxMilgramTarget.{u} := by
  intro V _ _ _ B hB F
  let f : V := (toDual Real V).symm F
  let e : V ≃L[Real] V := hB.continuousLinearEquivOfBilin
  refine ⟨e.symm f, ?_, ?_⟩
  · intro v
    rw [← hB.continuousLinearEquivOfBilin_apply]
    simp [e, f]
  · intro y hy
    apply e.injective
    apply ext_inner_right Real
    intro v
    rw [hB.continuousLinearEquivOfBilin_apply, hy v]
    simp [f]

#check laxMilgramDirect
#print axioms laxMilgramDirect

end Stage1Instances.THM_M_0329.Validation
