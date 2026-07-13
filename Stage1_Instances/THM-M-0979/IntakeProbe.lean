import Mathlib.Probability.Moments.SubGaussian
import Mathlib.Probability.Moments.Variance

/-!
# THM-M-0979 discovery-only intake probe

These checks authenticate pinned MGF, Chernoff, sub-Gaussian sum, independence, and variance
interfaces adjacent to possible Bernstein tail inequalities. `CandidateBoundedUpperTailShape`
keeps the unresolved leading prefactor explicit. It is a proposition definition, not the canonical
target, a theorem, or a proof of THM-M-0979.
-/

noncomputable section

open Finset MeasureTheory ProbabilityTheory Real
open scoped ENNReal NNReal MeasureTheory ProbabilityTheory

namespace Stage1Instances.THM_M_0979.Intake

universe u

/-- Finite range sum used only by the candidate intake shape. -/
def candidatePartialSum {Omega : Type u} (n : Nat) (X : Nat -> Omega -> Real)
    (omega : Omega) : Real :=
  Finset.sum (range n) fun i => X i omega

/-- Assumptions shared by one common bounded-summand Bernstein family. -/
structure CandidateBoundedProblem (Omega : Type u) [MeasurableSpace Omega] where
  mu : Measure Omega
  n : Nat
  X : Nat -> Omega -> Real
  varianceBudget : Real
  bound : Real
  isProbability : IsProbabilityMeasure mu
  varianceBudget_nonneg : 0 <= varianceBudget
  bound_nonneg : 0 <= bound
  aemeasurable : forall i, i < n -> AEMeasurable (X i) mu
  memLp_two : forall i, i < n -> MemLp (X i) 2 mu
  independent : iIndepFun X mu
  mean_zero : forall i, i < n -> mu[X i] = 0
  abs_bound_ae : forall i, i < n -> ∀ᵐ omega ∂mu, |X i omega| <= bound
  variance_sum_le : (Finset.sum (range n) fun i => Var[X i; mu]) <= varianceBudget

/--
Candidate binder shape only. The unresolved `prefactor` exposes a material difference between
inspected source and foreign-target surfaces rather than silently choosing one.
-/
def CandidateBoundedUpperTailShape (prefactor : Real) : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : CandidateBoundedProblem Omega) (t : Real),
      0 <= t ->
      P.mu.real {omega | t <= candidatePartialSum P.n P.X omega} <=
        prefactor * exp (-(t ^ 2) /
          (2 * (P.varianceBudget + P.bound * t / 3)))

#check ProbabilityTheory.mgf
#check ProbabilityTheory.cgf
#check ProbabilityTheory.measure_ge_le_exp_mul_mgf
#check ProbabilityTheory.measure_ge_le_exp_cgf
#check ProbabilityTheory.HasSubgaussianMGF.measure_sum_range_ge_le_of_iIndepFun
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.IndepFun.variance_sum
#check ProbabilityTheory.variance
#check CandidateBoundedUpperTailShape
#check CandidateBoundedUpperTailShape 1
#check CandidateBoundedUpperTailShape 2

end Stage1Instances.THM_M_0979.Intake
