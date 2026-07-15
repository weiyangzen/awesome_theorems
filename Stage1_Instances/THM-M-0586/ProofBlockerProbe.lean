import ObligationTree

/-!
# THM-M-0586: proof-availability blocker probe

This module checks that the two frozen terminal dimension packages are
equivalent to the canonical root and that mathlib's matching `proof_wanted`
markers are not retained declarations. It records a proof obstruction; it
does not prove the high-dimensional Poincare theorem.
-/

noncomputable section

namespace Stage1Instances.THMM0586

universe u

/-- The frozen immediate cut is root-equivalent: a root proof restricts to
dimension five and to dimensions at least six, while the checked composition
supplies the converse. -/
theorem dimension_packages_iff_target :
    (DimensionFivePackage.{u} ∧ StableDimensionPackage.{u}) ↔
      HighDimensionalPoincareTarget.{u} := by
  constructor
  · rintro ⟨dimensionFive, stable⟩
    exact highDimensionalPoincare_of_dimension_packages dimensionFive stable
  · intro root
    constructor
    · intro M _ _ _ _ _ e
      exact root 5 (by omega) M e
    · intro n hn M _ _ _ _ _ e
      exact root n (by omega) M e

#print axioms dimension_packages_iff_target

-- Batteries elaborates `proof_wanted` markers without modifying the
-- environment, so importing the mathlib module leaves these names absent.
#check_failure ContinuousMap.HomotopyEquiv.nonempty_homeomorph_sphere
#check_failure SimplyConnectedSpace.nonempty_homeomorph_sphere_three
#check_failure SimplyConnectedSpace.nonempty_diffeomorph_sphere_three

end Stage1Instances.THMM0586
