import Statement

/-!
# THM-M-1527 independent local validation probe

This module reconstructs the frozen conditional root directly from the two
fields of `CoordinateDecomposition`. It intentionally does not import
`Proof.lean` or `ObligationTree.lean`.
-/

noncomputable section

namespace Stage1Instances.THM_M_1527.Validation

open Stage1Instances.THM_M_1527

universe u

theorem independentMaxwellCoordinateEquivalence :
    MaxwellCoordinateEquivalence.{u} := by
  intro Spacetime _ _ ops c classical covariant _ _ _ _ _ decomposition
  constructor
  · rintro ⟨gaussElectric, gaussMagnetic, faraday, ampereMaxwell⟩
    exact ⟨decomposition.homogeneous_iff.mpr ⟨gaussMagnetic, faraday⟩,
      decomposition.inhomogeneous_iff.mpr ⟨gaussElectric, ampereMaxwell⟩⟩
  · rintro ⟨homogeneous, inhomogeneous⟩
    obtain ⟨gaussMagnetic, faraday⟩ := decomposition.homogeneous_iff.mp homogeneous
    obtain ⟨gaussElectric, ampereMaxwell⟩ :=
      decomposition.inhomogeneous_iff.mp inhomogeneous
    exact ⟨gaussElectric, gaussMagnetic, faraday, ampereMaxwell⟩

#print axioms independentMaxwellCoordinateEquivalence

end Stage1Instances.THM_M_1527.Validation
