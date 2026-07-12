import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1291: exact Brezis-Lieb statement

This module freezes the complex-valued, arbitrary-measure-space form of the
Brezis-Lieb lemma. It contains no proof of the lemma.
-/

namespace Stage1Instances.THM_M_1291

open Filter MeasureTheory
open scoped Topology

universe u

/-- The real `p`-power density used in the Brezis-Lieb identity. -/
noncomputable def pPower (p : ℝ) (g : α → ℂ) (x : α) : ℝ :=
  Real.rpow ‖g x‖ p

/-- Uniform boundedness of the real `p`-power integrals.

Integrability is included explicitly because Lean's Bochner integral is defined
to be zero for nonintegrable functions; an inequality between bare integrals
would therefore not faithfully express finite `L^p` mass.
-/
def UniformlyPPowerIntegrable {α : Type u} [MeasurableSpace α]
    (μ : Measure α) (p : ℝ) (f : ℕ → α → ℂ) : Prop :=
  ∃ C : ℝ, ∀ n : ℕ,
    Integrable (pPower p (f n)) μ ∧ ∫ x, pPower p (f n) x ∂μ ≤ C

/-- The integral-splitting conclusion, factored out only to keep mutation
declarations readable. -/
def SplittingLimit {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ)
    (f : α → ℂ) (fseq : ℕ → α → ℂ) : Prop :=
  Tendsto
    (fun n : ℕ ↦
      (∫ x, pPower p (fseq n) x ∂μ) -
        ∫ x, pPower p (fun y ↦ fseq n y - f y) x ∂μ)
    atTop (nhds (∫ x, pPower p f x ∂μ))

/-- The canonical complex-valued Brezis-Lieb target on an arbitrary measure
space. No finiteness or sigma-finiteness assumption is imposed on `μ`. -/
def BrezisLiebTarget : Prop :=
  ∀ {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ),
    0 < p →
    ∀ (f : α → ℂ) (fseq : ℕ → α → ℂ),
      (∀ n : ℕ, AEStronglyMeasurable (fseq n) μ) →
      (∀ᵐ x ∂μ, Tendsto (fun n : ℕ ↦ fseq n x) atTop (nhds (f x))) →
      UniformlyPPowerIntegrable μ p fseq →
      SplittingLimit μ p f fseq

/-- Fully expanded spelling used to check the selected encoding and binder
scope. -/
def ExpandedTarget : Prop :=
  ∀ {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ),
    0 < p →
    ∀ (f : α → ℂ) (fseq : ℕ → α → ℂ),
      (∀ n : ℕ, AEStronglyMeasurable (fseq n) μ) →
      (∀ᵐ x ∂μ, Tendsto (fun n : ℕ ↦ fseq n x) atTop (nhds (f x))) →
      (∃ C : ℝ, ∀ n : ℕ,
        Integrable (fun x ↦ Real.rpow ‖fseq n x‖ p) μ ∧
          (∫ x, Real.rpow ‖fseq n x‖ p ∂μ) ≤ C) →
      Tendsto
        (fun n : ℕ ↦
          (∫ x, Real.rpow ‖fseq n x‖ p ∂μ) -
            ∫ x, Real.rpow ‖fseq n x - f x‖ p ∂μ)
        atTop (nhds (∫ x, Real.rpow ‖f x‖ p ∂μ))

/-- Checked definitional transport to the fully expanded encoding. -/
theorem brezisLiebTarget_iff_expandedTarget :
    BrezisLiebTarget.{u} ↔ ExpandedTarget.{u} :=
  Iff.rfl

-- Structural mutations. These elaborate, but are intentionally not identified
-- with the canonical target.
def mutationAllowsZeroExponent : Prop :=
  ∀ {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ),
    0 ≤ p → ∀ (f : α → ℂ) (fseq : ℕ → α → ℂ),
      (∀ n, AEStronglyMeasurable (fseq n) μ) →
      (∀ᵐ x ∂μ, Tendsto (fun n ↦ fseq n x) atTop (nhds (f x))) →
      UniformlyPPowerIntegrable μ p fseq → SplittingLimit μ p f fseq

def mutationPointwiseEverywhere : Prop :=
  ∀ {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ),
    0 < p → ∀ (f : α → ℂ) (fseq : ℕ → α → ℂ),
      (∀ n, AEStronglyMeasurable (fseq n) μ) →
      (∀ x, Tendsto (fun n ↦ fseq n x) atTop (nhds (f x))) →
      UniformlyPPowerIntegrable μ p fseq → SplittingLimit μ p f fseq

def mutationRealValued : Prop :=
  ∀ {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ),
    0 < p → ∀ (f : α → ℝ) (fseq : ℕ → α → ℝ),
      (∀ n, AEStronglyMeasurable (fseq n) μ) →
      (∀ᵐ x ∂μ, Tendsto (fun n ↦ fseq n x) atTop (nhds (f x))) →
      (∃ C : ℝ, ∀ n,
        Integrable (fun x ↦ Real.rpow ‖fseq n x‖ p) μ ∧
          (∫ x, Real.rpow ‖fseq n x‖ p ∂μ) ≤ C) →
      Tendsto
        (fun n ↦ (∫ x, Real.rpow ‖fseq n x‖ p ∂μ) -
          ∫ x, Real.rpow ‖fseq n x - f x‖ p ∂μ)
        atTop (nhds (∫ x, Real.rpow ‖f x‖ p ∂μ))

def mutationBoundDependsOnIndex : Prop :=
  ∀ {α : Type u} [MeasurableSpace α] (μ : Measure α) (p : ℝ),
    0 < p → ∀ (f : α → ℂ) (fseq : ℕ → α → ℂ),
      (∀ n, AEStronglyMeasurable (fseq n) μ) →
      (∀ᵐ x ∂μ, Tendsto (fun n ↦ fseq n x) atTop (nhds (f x))) →
      (∀ n, ∃ C : ℝ, Integrable (pPower p (fseq n)) μ ∧
        ∫ x, pPower p (fseq n) x ∂μ ≤ C) → SplittingLimit μ p f fseq

end Stage1Instances.THM_M_1291

set_option pp.explicit true in
#print Stage1Instances.THM_M_1291.BrezisLiebTarget
