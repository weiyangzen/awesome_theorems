import Mathlib.Probability.Distributions.Gaussian.Multivariate

/-!
# THM-M-0996 proof attempt

This module contains the proof-phase result that can currently be justified
against the frozen target: the zero-dimensional branch is impossible because
a unit-norm continuous linear functional cannot exist on a subsingleton
space. The positive-dimensional Gaussian isoperimetric branch remains open.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0996

universe u

def IsUnitHalfspace {E : Type u} [NormedAddCommGroup E]
    [NormedSpace Real E] (H : Set E) : Prop :=
  exists (L : E →L[Real] Real) (c : Real), ‖L‖ = 1 /\ H = {x | L x <= c}

def GaussianIsoperimetricTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (A H : Set E),
      MeasurableSet A -> IsUnitHalfspace H ->
      stdGaussian E A = stdGaussian E H ->
      forall r : Real, 0 < r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A)

/-- The dimension-zero branch of the frozen target is vacuous: in dimension
zero every vector is zero, so every continuous linear functional has norm
zero and cannot be a unit-normal witness. -/
theorem no_unitHalfspace_of_finrank_zero
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] (hE : Module.finrank Real E = 0) :
    forall H : Set E, ¬ IsUnitHalfspace H := by
  letI : Subsingleton E := (Module.finrank_zero_iff.mp hE)
  intro H hH
  obtain ⟨L, c, hL, hH⟩ := hH
  have hLzero : L = 0 := by
    ext x
    rw [Subsingleton.elim x 0]
    exact L.map_zero
  have : (0 : Real) = 1 := by
    rw [hLzero, norm_zero] at hL
    exact hL
  norm_num at this

/-- Kernel-checked closure of the complete canonical comparison in the
zero-dimensional branch. -/
theorem target_of_finrank_zero
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [MeasurableSpace E] [BorelSpace E] [FiniteDimensional Real E]
    (hE : Module.finrank Real E = 0) (A H : Set E) :
    MeasurableSet A -> IsUnitHalfspace H ->
      stdGaussian E A = stdGaussian E H ->
      forall r : Real, 0 < r ->
        stdGaussian E (Metric.thickening r H) <=
          stdGaussian E (Metric.thickening r A) := by
  intro _ hH
  exact (no_unitHalfspace_of_finrank_zero E hE H hH).elim

end Stage1Instances.THM_M_0996

#print axioms Stage1Instances.THM_M_0996.no_unitHalfspace_of_finrank_zero
#print axioms Stage1Instances.THM_M_0996.target_of_finrank_zero
