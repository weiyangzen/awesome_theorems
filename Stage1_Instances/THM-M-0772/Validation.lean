import Mathlib.Order.Zorn

/-!
# THM-M-0772 independent validation probe

This module deliberately does not import the dossier proof or obligation-tree
module. It obtains the same exact existence result through the separately
implemented `IsChain.exists_maxChain` API.
-/

namespace Stage1Instances.THM_M_0772.Validation

universe u

def ValidationTarget : Prop :=
  ∀ (P : Type u) [PartialOrder P], ∃ c : Set P, IsMaxChain (· ≤ ·) c

theorem independentHausdorffMaximalPrinciple : ValidationTarget.{u} := by
  intro P _order
  obtain ⟨c, hc, _empty_subset⟩ :=
    (@IsChain.empty P (fun x y => x <= y)).exists_maxChain
  exact ⟨c, hc⟩

end Stage1Instances.THM_M_0772.Validation

#print axioms Stage1Instances.THM_M_0772.Validation.independentHausdorffMaximalPrinciple
