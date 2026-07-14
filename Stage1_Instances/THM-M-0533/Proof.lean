import ObligationTree

/-!
# THM-M-0533 partial proof execution

This module proves the elementary signed-map identity required by the frozen
construction package. It does not construct the connecting maps or prove any
of the exactness packages, so the Mayer-Vietoris root remains open.
-/

open CategoryTheory CategoryTheory.Limits
open TopologicalSpace

namespace AwesomeTheorems.THM_M_0533

universe u

noncomputable section

/-- The two inclusion-induced maps in the frozen Mayer-Vietoris sequence have
zero composite. -/
theorem firstMap_comp_secondMap {X : TopCat.{u}} (U V : Opens X) (n : Nat) :
    firstMap U V n ≫ secondMap U V n = 0 := by
  have hinc : interLeft U V ≫ Opens.inclusion' U =
      interRight U V ≫ Opens.inclusion' V := by
    ext x
    rfl
  simp [firstMap, secondMap, ← Functor.map_comp, hinc]

#print axioms firstMap_comp_secondMap

end

end AwesomeTheorems.THM_M_0533
