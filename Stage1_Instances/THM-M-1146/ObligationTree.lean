import Statement

/-!
# THM-M-1146 conditional obligation composition

This module checks the final composition interface selected before proof work.
The harmonicity of the reflected function remains an explicit package premise.
-/

namespace Stage1Instances.THM_M_1146

open Complex InnerProductSpace
open scoped ComplexConjugate

noncomputable section

/-- Output required from the conjugation, lower-branch, and boundary-gluing obligations. -/
def ReflectedHarmonicPackage : Prop :=
  ∀ (V : Set Complex) (u : Complex -> Real),
    IsOpen V ->
    (∀ z, z ∈ V ↔ starRingEnd Complex z ∈ V) ->
    HarmonicOnNhd u (upperPart V) ->
    ContinuousOn u (upperPart V ∪ reflectingPart V) ->
    (∀ z ∈ reflectingPart V, u z = 0) ->
    HarmonicOnNhd (oddReflection u) V

/-- Checked conditional composition from the analytic package to the exact frozen root. -/
theorem schwarzReflectionTarget_of_reflectedHarmonicPackage
    (harmonicReflection : ReflectedHarmonicPackage) : SchwarzReflectionTarget := by
  intro V u hV hsym hu hcont hzero
  refine ⟨harmonicReflection V u hV hsym hu hcont hzero, ?_⟩
  intro z hz
  exact oddReflection_eq_of_nonnegative_imaginary u z (le_of_lt hz.2)

#print axioms schwarzReflectionTarget_of_reflectedHarmonicPackage

end
end Stage1Instances.THM_M_1146
