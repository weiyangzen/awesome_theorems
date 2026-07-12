import Statement

/-!
# THM-M-0158 conditional obligation composition

The substantive differential-geometric derivation remains an explicit premise.
This module checks only its composition into the exact frozen target.
-/

namespace Stage1Instances.THM_M_0158

/-- Output contract of the open tangency, differentiated-orthogonality,
Gram-solve, and vector-reconstruction obligations. -/
def WeingartenDerivationPackage : Prop :=
  forall (U : Set ParameterSpace) (x N : ParameterSpace -> AmbientSpace) (p : ParameterSpace),
    IsOpen U -> p ∈ U -> ContDiffOn Real 2 x U -> ContDiffOn Real 1 N U ->
    (forall q, q ∈ U -> ‖N q‖ = 1) ->
    (forall q, q ∈ U -> forall i : Fin 2,
      @inner Real AmbientSpace _ (N q) (partialWithin U x i q) = 0) ->
    Matrix.det (firstFundamentalForm U x p) ≠ 0 ->
    forall i : Fin 2,
      partialWithin U N i p =
        ∑ j : Fin 2,
          (-(firstFundamentalForm U x p)⁻¹ * secondFundamentalForm U x N p) j i •
            partialWithin U x j p

/-- Checked conditional assembly into the exact canonical root. -/
theorem root_of_derivation_package
    (derivation : WeingartenDerivationPackage) : WeingartenEquationsTarget := by
  exact derivation

#print axioms root_of_derivation_package

end Stage1Instances.THM_M_0158
