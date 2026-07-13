import Statement

/-!
# THM-M-0417 independent kernel-validation probe

This module reconstructs the exact frozen target directly from the pinned
mathlib terminal declaration. It deliberately does not import `Proof.lean` or
`ObligationTree.lean`. This is same-workspace corroboration, not the distinct
runner required by rev-5.6 section 10.7.
-/

namespace Stage1Instances.THM_M_0417.Validation

open MeasureTheory Module

universe u

/-- A separately implemented proof of the exact frozen strict Minkowski target. -/
theorem independentMinkowskiConvexBody :
    Stage1Instances.THM_M_0417.Statement.{u} := by
  intro E _ _ _ _ _ mu _ L _ F s fund hSymm hConv hMeasure
  exact MeasureTheory.exists_ne_zero_mem_lattice_of_measure_mul_two_pow_lt_measure
    fund hSymm hConv hMeasure

#check independentMinkowskiConvexBody
#print axioms independentMinkowskiConvexBody

end Stage1Instances.THM_M_0417.Validation
