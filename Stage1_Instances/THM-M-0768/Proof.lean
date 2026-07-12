import ObligationTree

/-!
# THM-M-0768 proof-phase bodies

The pinned mathlib theorem supplies the frozen relation-preserving bridge.  The canonical
raw-function target is then obtained through the specialization already checked in the frozen
obligation architecture.
-/

namespace Stage1Instances.THM_M_0768

open Function

universe u v

/-- Exact local wrapper around mathlib's stronger relation-preserving theorem. -/
theorem relationalPackage_proof : RelationalPackage.{u, v} := by
  intro alpha beta f g hf hg R hfR hgR
  exact Function.Embedding.schroeder_bernstein_of_rel hf hg R hfR hgR

/-- Exact proof of the canonical proposition frozen in `Statement.lean`. -/
theorem cantorBernsteinSchroeder_proof : CantorBernsteinSchroederTarget.{u, v} :=
  root_of_relational_package relationalPackage_proof

#print axioms Function.Embedding.schroeder_bernstein_of_rel
#print axioms relationalPackage_proof
#print axioms cantorBernsteinSchroeder_proof

end Stage1Instances.THM_M_0768
