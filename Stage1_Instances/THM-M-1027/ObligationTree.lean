import Statement

/-!
# THM-M-1027 conditional composition certificate

This module checks the witness-to-root interface. It deliberately does not
construct a Wiener process or import the external Brownian-motion project.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_1027

universe u

/-- A fully assembled witness package for the frozen existential target. -/
structure WienerWitnessPackage where
  Omega : Type u
  measurableSpace : MeasurableSpace Omega
  P : @Measure Omega measurableSpace
  W : Time -> Omega -> Real
  probability : @IsProbabilityMeasure Omega measurableSpace P
  laws : @IsWienerProcess Omega measurableSpace P W

/-- Exact conditional composition from an assembled witness to the frozen root. -/
theorem wienerExistenceTarget_of_witnessPackage
    (package : WienerWitnessPackage.{u}) : WienerExistenceTarget.{u} := by
  exact ⟨package.Omega, package.measurableSpace, package.P, package.W,
    package.probability, package.laws⟩

#print axioms wienerExistenceTarget_of_witnessPackage

end Stage1Instances.THM_M_1027
