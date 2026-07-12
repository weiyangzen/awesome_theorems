import «Stage1_Instances».«THM-M-1518».Statement

/-!
Conditional composition certificate for the frozen THM-M-1518 proof
architecture. The first-variation identity and weak-to-pointwise analytic
bridge are explicit premises; this file does not prove either package.
-/

noncomputable section

open Set MeasureTheory

namespace Stage1Instances.THM_M_1518.ObligationTree

/-- The weak Euler-Lagrange equation before integration by parts and the
fundamental lemma have produced a pointwise identity. -/
def WeakEulerLagrange {n : Nat}
    (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n) : Prop :=
  ∀ η : Path n, AdmissibleVariation B η →
    ∫ t in B.initialTime..B.finalTime,
      PositionDerivative L t (q t) (deriv q t) (η t) +
        VelocityDerivative L t (q t) (deriv q t) (deriv η t) = 0

/-- The analytic identity obtained by differentiating the action under the
integral sign. -/
def FirstVariationFormula : Prop :=
  ∀ (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L → ContDiff ℝ 2 q →
        ∀ η : Path n, AdmissibleVariation B η →
          FirstVariation L B q η =
            ∫ t in B.initialTime..B.finalTime,
              PositionDerivative L t (q t) (deriv q t) (η t) +
                VelocityDerivative L t (q t) (deriv q t) (deriv η t)

/-- The combined integration-by-parts and fundamental-lemma package. It is
kept open and expanded into separate frozen child obligations in the registry. -/
def WeakToPointwise : Prop :=
  ∀ (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n),
      ContDiff ℝ 2 L → ContDiff ℝ 2 q →
        WeakEulerLagrange L B q → EulerLagrangeEquation L B q

/-- Checked child-to-parent composition into the exact frozen target. -/
theorem exactTarget_of_packages
    (variation : FirstVariationFormula)
    (weakToPointwise : WeakToPointwise) :
    StationaryActionEulerLagrangeTarget := by
  intro n L B q hL hq _ _ hstationary
  apply weakToPointwise n L B q hL hq
  intro η hη
  rw [← variation n L B q hL hq η hη]
  exact hstationary η hη

#check exactTarget_of_packages
#print axioms exactTarget_of_packages

end Stage1Instances.THM_M_1518.ObligationTree
