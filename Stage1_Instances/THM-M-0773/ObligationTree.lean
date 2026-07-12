import Statement

/-!
# THM-M-0773 conditional obligation composition

This module checks the structural passage from the pointed maximal-extension
package to the frozen nonempty-family target. The substantive pointed package
remains an explicit premise, so this architecture file claims no root proof.
-/

open Set

universe u

namespace Stage1Instances.THM_M_0773.ObligationTree

/-- The substantive pointed package supplied by the pinned mathlib anchor. -/
def PointedMaximalPackage : Prop :=
  forall (alpha : Type u) (F : Set (Set alpha)),
    Order.IsOfFiniteCharacter F ->
    forall x, x ∈ F -> exists m, x ⊆ m ∧ Maximal (fun y => y ∈ F) m

/-- Select a seed, invoke the explicit pointed package, and forget extension. -/
theorem root_of_pointedPackage
    (pointed : PointedMaximalPackage.{u}) :
    Stage1Instances.THM_M_0773.TeichmullerTukeyTarget.{u} := by
  intro alpha F hfinite hne
  obtain ⟨x, hx⟩ := hne
  obtain ⟨m, _hxm, hm⟩ := pointed alpha F hfinite x hx
  exact ⟨m, hm⟩

#check root_of_pointedPackage
#print axioms root_of_pointedPackage

end Stage1Instances.THM_M_0773.ObligationTree
