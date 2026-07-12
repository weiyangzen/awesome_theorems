import Statement

/-!
# THM-M-1244 conditional obligation composition

This module checks how two still-open analytic packages compose to the exact
canonical target. It does not construct either package.
-/

namespace Stage1Instances.THM_M_1244

open MeasureTheory
open scoped BigOperators

/-- The coordinate-gradient energy used by the audited upstream theorem. -/
noncomputable def coordinateEnergy {n : Nat} (f : Euclidean n -> Real)
    (x : Euclidean n) : Real :=
  ∑ i : Fin n, (fderiv Real f x (Pi.single i 1)) ^ 2

/-- Open package containing the source theorem after measure, entropy, and
regularity transports, but before changing its energy encoding. -/
def CoordinateLogSobolevPackage : Prop :=
  forall (n : Nat) (f : Euclidean n -> Real),
    ContDiff Real 1 f ->
    Integrable (fun x => f x ^ 2) (standardGaussian n) ->
    Integrable (fun x => xlogx (f x ^ 2)) (standardGaussian n) ->
    Integrable (fun x => norm (fderiv Real f x) ^ 2) (standardGaussian n) ->
    entropySquare f (standardGaussian n) <=
      2 * ∫ x, coordinateEnergy f x ∂(standardGaussian n)

/-- Open package asserting the direction actually needed to pass from the
coordinate-square energy to the canonical operator-norm energy. -/
def CoordinateToOperatorEnergyPackage : Prop :=
  forall (n : Nat) (f : Euclidean n -> Real),
    ContDiff Real 1 f ->
    Integrable (fun x => f x ^ 2) (standardGaussian n) ->
    Integrable (fun x => xlogx (f x ^ 2)) (standardGaussian n) ->
    Integrable (fun x => norm (fderiv Real f x) ^ 2) (standardGaussian n) ->
    2 * (∫ x, coordinateEnergy f x ∂(standardGaussian n)) <=
      2 * ∫ x, norm (fderiv Real f x) ^ 2 ∂(standardGaussian n)

/-- Checked child-to-root composition. Both substantive packages are explicit
premises and therefore remain in the root cut set. -/
theorem gaussianLogSobolevTarget_of_packages
    (coordinateLSI : CoordinateLogSobolevPackage)
    (energyBridge : CoordinateToOperatorEnergyPackage) :
    GaussianLogSobolevTarget := by
  intro n f hf hsq hent henergy
  exact (coordinateLSI n f hf hsq hent henergy).trans
    (energyBridge n f hf hsq hent henergy)

#print axioms gaussianLogSobolevTarget_of_packages

end Stage1Instances.THM_M_1244
