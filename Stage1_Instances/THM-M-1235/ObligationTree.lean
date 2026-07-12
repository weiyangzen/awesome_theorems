import Statement

/-!
# THM-M-1235 conditional obligation composition

This module checks only the final composition selected by the frozen proof
architecture. Existence and uniqueness remain explicit hypotheses; no proof of
Wolibner's analytic argument is asserted here.
-/

namespace Stage1Instances.THMM1235

/-- Existence package for the exact source data and conditions frozen in the
canonical statement. -/
def WolibnerExistencePackage : Prop :=
  forall (D : SourceData) (T : Real),
    D.domain.isClosedPlanarRegion ->
    D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
    D.vorticityLebesgueIntegrableOnDomain ->
    D.vorticityHasSourceDecay ->
    D.vorticityIsHolderContinuous ->
    D.initialCirculationOnEveryInteriorBoundaryComponentIsZero ->
    0 < T -> Nonempty (Motion D T)

/-- Uniqueness package for motions satisfying the same eight source
conditions. -/
def WolibnerUniquenessPackage : Prop :=
  forall (D : SourceData) (T : Real),
    D.domain.isClosedPlanarRegion ->
    D.domain.boundaryIsFiniteUnionOfClosedAnalyticCurves ->
    D.vorticityLebesgueIntegrableOnDomain ->
    D.vorticityHasSourceDecay ->
    D.vorticityIsHolderContinuous ->
    D.initialCirculationOnEveryInteriorBoundaryComponentIsZero ->
    0 < T -> forall S₁ S₂ : Motion D T, SameMotion S₁ S₂

/-- Checked composition into the exact canonical root. Both substantive
packages are consumed, and no additional mathematical premise is introduced. -/
theorem root_of_existence_and_uniqueness
    (existence : WolibnerExistencePackage)
    (uniqueness : WolibnerUniquenessPackage) :
    WolibnerGlobalExistenceAndUniqueness := by
  intro D T hDomain hBoundary hIntegrable hDecay hHolder hCirculation hT
  obtain ⟨S⟩ := existence D T hDomain hBoundary hIntegrable hDecay hHolder
    hCirculation hT
  exact ⟨S, fun S' => uniqueness D T hDomain hBoundary hIntegrable hDecay
    hHolder hCirculation hT S' S⟩

#print axioms root_of_existence_and_uniqueness

end Stage1Instances.THMM1235
