import Statement

/-!
# THM-M-1006 conditional obligation composition

The two directions of the discrete BDG comparison remain explicit premises.
This module checks only that independently uniform constants for those
directions compose into the exact frozen target.
-/

open MeasureTheory

namespace Stage1Instances.THM_M_1006

universe u

/-- The lower (square-function to maximal-function) half of the frozen target. -/
def LowerBDG (p : Real) : Prop :=
  0 < p ->
    exists c : ENNReal, 0 < c /\ c < ⊤ /\
      forall (Omega : Type u) (m : MeasurableSpace Omega) (mu : Measure Omega),
        @IsProbabilityMeasure Omega m mu ->
        forall (F : Filtration Nat m) (f : Nat -> Omega -> Real),
          Martingale f F mu -> f 0 = 0 -> forall n : Nat,
            c * ∫⁻ omega, (ENNReal.ofReal (quadraticVariation f n omega)).rpow (p / 2) ∂mu <=
              ∫⁻ omega, (ENNReal.ofReal (maximalProcess f n omega)).rpow p ∂mu

/-- The upper (maximal-function to square-function) half of the frozen target. -/
def UpperBDG (p : Real) : Prop :=
  0 < p ->
    exists C : ENNReal, 0 < C /\ C < ⊤ /\
      forall (Omega : Type u) (m : MeasurableSpace Omega) (mu : Measure Omega),
        @IsProbabilityMeasure Omega m mu ->
        forall (F : Filtration Nat m) (f : Nat -> Omega -> Real),
          Martingale f F mu -> f 0 = 0 -> forall n : Nat,
            ∫⁻ omega, (ENNReal.ofReal (maximalProcess f n omega)).rpow p ∂mu <=
              C * ∫⁻ omega, (ENNReal.ofReal (quadraticVariation f n omega)).rpow (p / 2) ∂mu

/-- Checked conditional composition of both BDG directions into `StatementShape`. -/
theorem root_of_directional_BDG
    (lower : forall p : Real, LowerBDG.{u} p)
    (upper : forall p : Real, UpperBDG.{u} p) :
    forall p : Real, StatementShape.{u} p := by
  intro p hp
  obtain ⟨c, hc0, hcTop, hc⟩ := lower p hp
  obtain ⟨C, hC0, hCTop, hC⟩ := upper p hp
  refine ⟨c, C, hc0, hcTop, hC0, hCTop, ?_⟩
  intro Omega m mu hmu F f hf hf0 n
  exact ⟨hc Omega m mu hmu F f hf hf0 n, hC Omega m mu hmu F f hf hf0 n⟩

#print axioms root_of_directional_BDG

end Stage1Instances.THM_M_1006
