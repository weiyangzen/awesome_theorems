import Mathlib.Analysis.Matrix.Normed
import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.LinearAlgebra.DFinsupp
import Mathlib.MeasureTheory.Function.L1Space.Integrable
import Mathlib.Topology.MetricSpace.Pseudo.Defs

/-!
# Exact statement target for THM-M-1419

This file freezes the finite-dimensional real, invertible, ergodic, two-sided
splitting form of Oseledets' multiplicative ergodic theorem.  It declares the
target proposition only; it does not assert or prove that proposition.
-/

noncomputable section

open Filter MeasureTheory
open scoped Matrix.Norms.Operator Topology

namespace Stage1Instances.THM_M_1419

/-- The standard finite-dimensional real coordinate space. -/
abbrev Vector (d : ℕ) := Fin d → ℝ

/-- Real square matrices acting on the coordinate space. -/
abbrev SquareMatrix (d : ℕ) := _root_.Matrix (Fin d) (Fin d) ℝ

/-- `log⁺ x = log (max 1 x)`, used in the moment hypotheses. -/
def logPlus (x : ℝ) : ℝ := Real.log (max 1 x)

/-- Forward ordered product `A(T^(n-1)ω) ... A(Tω) A(ω)`. -/
def cocycleProduct {Ω : Type*} (T : Ω → Ω) (A : Ω → SquareMatrix d) :
    ℕ → Ω → SquareMatrix d
  | 0, _ => 1
  | n + 1, ω => A ((T^[n]) ω) * cocycleProduct T A n ω

/--
Concrete measurability predicate for a finite-dimensional subspace field.
Distance-to-the-fiber measurability avoids postulating an arbitrary measurable
space on `Submodule ℝ (Fin d → ℝ)`.
-/
def MeasurableSubspaceField {Ω : Type*} [MeasurableSpace Ω]
    (E : Ω → Fin k → Submodule ℝ (Vector d)) : Prop :=
  ∀ i v, Measurable fun ω => Metric.infDist v (E ω i : Set (Vector d))

/--
The exact selected target.

It is the invertible ergodic probability-space form: both the matrix and its
inverse satisfy logarithmic moment conditions; the conclusion is a measurable
invariant direct-sum splitting into nonzero subspaces with strictly decreasing
constant Lyapunov exponents, and one common conull set supports the growth
limit for every nonzero vector in every fiber.
-/
def OseledetsMultiplicativeErgodicTarget : Prop :=
  ∀ (d : ℕ), 0 < d →
  ∀ (Ω : Type*) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Ω ≃ Ω) (A : Ω → SquareMatrix d),
    MeasurePreserving T μ μ →
    Ergodic T μ →
    AEStronglyMeasurable A μ →
    AEStronglyMeasurable (fun ω => (A ω)⁻¹) μ →
    (∀ᵐ ω ∂μ, IsUnit (A ω)) →
    Integrable (fun ω => logPlus ‖A ω‖) μ →
    Integrable (fun ω => logPlus ‖(A ω)⁻¹‖) μ →
    ∃ (k : ℕ) (exponents : Fin k → ℝ)
      (E : Ω → Fin k → Submodule ℝ (Vector d)),
      0 < k ∧
      StrictAnti exponents ∧
      MeasurableSubspaceField E ∧
      (∀ᵐ ω ∂μ,
        iSupIndep (E ω) ∧
        (⨆ i, E ω i) = ⊤ ∧
        (∀ i, 0 < Module.finrank ℝ (E ω i)) ∧
        (∀ i, Submodule.map (Matrix.mulVecLin (A ω)) (E ω i) = E (T ω) i) ∧
        ∀ i v, v ∈ E ω i → v ≠ 0 →
          Tendsto
            (fun n : ℕ => ((n : ℝ)⁻¹ * Real.log ‖(cocycleProduct T A n ω).mulVec v‖))
            atTop (nhds (exponents i)))

/-! Statement mutations are deliberately noncanonical.  Printing them beside
the target makes dropped hypotheses and changed domains visible to review. -/

/-- Mutation: deletes inverse measurability and inverse logarithmic integrability. -/
def MutationWithoutInverseMoment : Prop :=
  ∀ (d : ℕ), 0 < d →
  ∀ (Ω : Type*) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Ω ≃ Ω) (A : Ω → SquareMatrix d),
    MeasurePreserving T μ μ → Ergodic T μ → AEStronglyMeasurable A μ →
    (∀ᵐ ω ∂μ, IsUnit (A ω)) →
    Integrable (fun ω => logPlus ‖A ω‖) μ → True

/-- Mutation: changes the invertible base to a one-sided endomorphism. -/
def MutationOneSidedBase : Prop :=
  ∀ (d : ℕ), 0 < d →
  ∀ (Ω : Type*) [MeasurableSpace Ω] (μ : Measure Ω) [IsProbabilityMeasure μ]
    (T : Ω → Ω) (A : Ω → SquareMatrix d),
    MeasurePreserving T μ μ → Ergodic T μ → AEStronglyMeasurable A μ → True

#check OseledetsMultiplicativeErgodicTarget
#check @OseledetsMultiplicativeErgodicTarget
set_option pp.universes true in
#print OseledetsMultiplicativeErgodicTarget
set_option pp.universes true in
#print MutationWithoutInverseMoment
set_option pp.universes true in
#print MutationOneSidedBase

end Stage1Instances.THM_M_1419
