import «Stage1_Instances».«THM-M-1524».Statement

/-!
Checked leaves and conditional composition for the frozen THM-M-1524
architecture. The Robertson and CCR packages remain explicit premises.
-/

noncomputable section

namespace Stage1Instances.THM_M_1524.ObligationTree

universe u

variable {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- The Cauchy-Schwarz leaf used after both observable vectors are centered. -/
theorem centered_cauchy_schwarz (x y : H) :
    ‖inner ℂ x y‖ ≤ ‖x‖ * ‖y‖ :=
  norm_inner_le_norm x y

/-- Checked child-to-parent composition into the exact two-component target. -/
theorem exactTarget_of_components
    (robertson : RobertsonTarget.{u})
    (ccr : HeisenbergCCRTarget.{u}) :
    HeisenbergUncertaintyTarget.{u} :=
  ⟨robertson, ccr⟩

#check centered_cauchy_schwarz
#check exactTarget_of_components
#print axioms centered_cauchy_schwarz
#print axioms exactTarget_of_components

end Stage1Instances.THM_M_1524.ObligationTree
