import Statement

/-!
# THM-M-0773 proof-phase bodies

The substantive pointed obligation is discharged by the theorem in the pinned
`Mathlib.Order.TeichmullerTukey` module.  The exact frozen root then follows by
the already checked pointed-to-unpointed transport.
-/

open Set

universe u

namespace Stage1Instances.THM_M_0773

/-- Every member of a finite-character family extends to a maximal member. -/
theorem pointed_maximal_proof : PointedTarget.{u} := by
  intro alpha F hfinite x hx
  exact hfinite.exists_maximal hx

/-- Exact proof of the canonical nonempty-family target frozen in `Statement.lean`. -/
theorem teichmullerTukey_proof : TeichmullerTukeyTarget.{u} := by
  exact pointed_implies_unpointed pointed_maximal_proof

#check pointed_maximal_proof
#check teichmullerTukey_proof
#print axioms pointed_maximal_proof
#print axioms teichmullerTukey_proof

end Stage1Instances.THM_M_0773
