import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0533 same-worker differential validation

This module imports neither `Proof` nor `ObligationTree`. It independently
reconstructs the one elementary signed-map identity claimed by the proof
receipt. It does not construct the connecting morphisms, exactness packages,
or the canonical Mayer-Vietoris root.
-/

open CategoryTheory CategoryTheory.Limits
open TopologicalSpace

namespace AwesomeTheorems.THM_M_0533.Validation

universe u

noncomputable section

/-- A separately written check that the two inclusion-induced maps cancel. -/
theorem independentlyReconstructedFirstSecond {X : TopCat.{u}}
    (U V : Opens X) (n : Nat) :
    firstMap U V n ≫ secondMap U V n = 0 := by
  have hleft : interLeft U V ≫ Opens.inclusion' U =
      interRight U V ≫ Opens.inclusion' V := by
    ext x
    rfl
  rw [show firstMap U V n = biprod.lift
      ((HFunctor n).map (interLeft U V))
      (-((HFunctor n).map (interRight U V))) by rfl]
  rw [show secondMap U V n = biprod.desc
      ((HFunctor n).map (Opens.inclusion' U))
      ((HFunctor n).map (Opens.inclusion' V)) by rfl]
  rw [biprod.lift_desc, Preadditive.neg_comp, ← Functor.map_comp,
    ← Functor.map_comp, hleft, add_neg_cancel]

end

assert_no_sorry independentlyReconstructedFirstSecond
#check independentlyReconstructedFirstSecond
#print sorries independentlyReconstructedFirstSecond
#print axioms independentlyReconstructedFirstSecond

end AwesomeTheorems.THM_M_0533.Validation
