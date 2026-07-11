import Statement
import ObligationTree

/-!
# THM-M-0087 proof execution

This module integrates the Gabriel-Popescu proof bodies from the repository's
pinned mathlib revision.  The four named packages mirror the frozen obligation
branches, and `gabrielPopescu_via_frozen_composition` checks their exact
child-to-root composition.
-/

noncomputable section

open CategoryTheory CategoryTheory.Limits

universe v u

namespace Stage1Instances.THM_M_0087.Proof

variable (C : Type u) [Category.{v} C] [Abelian C]
  [IsGrothendieckAbelian.{v} C]

/-- Fullness, backed by the pinned Gabriel-Popescu construction. -/
theorem fullPackage : ObligationTree.FullPackage C := by
  intro G hG
  exact IsGrothendieckAbelian.GabrielPopescu.full G hG

/-- Faithfulness is the separator characterization of preadditive coyoneda. -/
theorem faithfulPackage : ObligationTree.FaithfulPackage C := by
  intro G hG
  exact (isSeparator_iff_faithful_preadditiveCoyonedaObj G).1 hG

/-- The pinned tensor construction carries the required tensor-Hom adjunction. -/
theorem adjunctionPackage : ObligationTree.AdjunctionPackage C := by
  intro G _
  exact ⟨IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction G⟩

/-- Exactness is represented by finite-limit preservation in the frozen target. -/
theorem finiteLimitsPackage : ObligationTree.FiniteLimitsPackage C := by
  intro G hG
  exact IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits G hG

/-- Exact frozen root, assembled through the obligation-tree certificate. -/
theorem gabrielPopescu_via_frozen_composition : Statement C :=
  ObligationTree.root_of_packages C
    (fullPackage C) (faithfulPackage C) (adjunctionPackage C)
      (finiteLimitsPackage C)

/-- A direct exact-target wrapper, retained as an independent type check. -/
theorem gabrielPopescu : Statement C := by
  intro G hG
  exact
    ⟨IsGrothendieckAbelian.GabrielPopescu.full G hG,
      (isSeparator_iff_faithful_preadditiveCoyonedaObj G).1 hG,
      ⟨IsGrothendieckAbelian.tensorObjPreadditiveCoyonedaObjAdjunction G⟩,
      IsGrothendieckAbelian.GabrielPopescu.preservesFiniteLimits G hG⟩

#print axioms fullPackage
#print axioms faithfulPackage
#print axioms adjunctionPackage
#print axioms finiteLimitsPackage
#print axioms gabrielPopescu_via_frozen_composition
#print axioms gabrielPopescu
#print axioms IsGrothendieckAbelian.GabrielPopescuAux.kernel_ι_d_comp_d
#print axioms IsGrothendieckAbelian.GabrielPopescuAux.exists_d_comp_eq_d
#print axioms IsGrothendieckAbelian.GabrielPopescu.preservesInjectiveObjects

end Stage1Instances.THM_M_0087.Proof
