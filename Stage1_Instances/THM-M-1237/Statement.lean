import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.Topology.MetricSpace.Holder

/-!
The exact statement node for THM-M-1237.  It selects the supercritical,
first-order Morrey-Sobolev embedding on a bounded domain equipped with explicit
`W^{1,p}` extension data.  The extension data is part of the hypotheses, rather
than an opaque assertion that the domain is regular.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal NNReal Topology

namespace Stage1Rev56.THMM1237

abbrev Space (n : ℕ) := EuclideanSpace ℝ (Fin n)

def unitVector {n : ℕ} (i : Fin n) : Space n :=
  EuclideanSpace.single i 1

def spatialDerivative {n : ℕ} (f : Space n → ℝ) (i : Fin n) (x : Space n) : ℝ :=
  fderiv ℝ f x (unitVector i)

def SmoothCompactTest {n : ℕ} (φ : Space n → ℝ) : Prop :=
  ContDiff ℝ ⊤ φ ∧ HasCompactSupport φ

/-- Distributional first derivative on a measurable domain. -/
def IsWeakDerivativeOn {n : ℕ} (Ω : Set (Space n))
    (u : Space n → ℝ) (du : Space n → Fin n → ℝ) : Prop :=
  ∀ (i : Fin n) (φ : Space n → ℝ), SmoothCompactTest φ →
    (∫ x in Ω, du x i * φ x) = -(∫ x in Ω, u x * spatialDerivative φ i x)

/-- Concrete scalar `W^{1,p}(Ω)` data used by the statement. -/
structure W1pData {n : ℕ} (Ω : Set (Space n)) (p : ℝ≥0) : Type where
  function : Space n → ℝ
  weakGradient : Space n → Fin n → ℝ
  functionMemLp : MemLp function (p : ℝ≥0∞) (volume.restrict Ω)
  gradientMemLp : MemLp weakGradient (p : ℝ≥0∞) (volume.restrict Ω)
  isWeakDerivative : IsWeakDerivativeOn Ω function weakGradient

/-- A specified bounded extension operator package for one `W^{1,p}` input. -/
structure ExtensionData {n : ℕ} {Ω : Set (Space n)} {p : ℝ≥0}
    (u : W1pData Ω p) : Type where
  extendedFunction : Space n → ℝ
  extendedGradient : Space n → Fin n → ℝ
  agreesOnDomain : ∀ᵐ x ∂volume.restrict Ω, extendedFunction x = u.function x
  functionMemLp : MemLp extendedFunction (p : ℝ≥0∞) volume
  gradientMemLp : MemLp extendedGradient (p : ℝ≥0∞) volume
  isWeakDerivative : IsWeakDerivativeOn Set.univ extendedFunction extendedGradient
  operatorBound : ℝ≥0
  normBound :
    eLpNorm extendedFunction (p : ℝ≥0∞) volume +
        eLpNorm extendedGradient (p : ℝ≥0∞) volume ≤
      operatorBound *
        (eLpNorm u.function (p : ℝ≥0∞) (volume.restrict Ω) +
          eLpNorm u.weakGradient (p : ℝ≥0∞) (volume.restrict Ω))

/-- The Holder representative and quantitative Morrey estimate. -/
structure HolderRepresentative {n : ℕ} {Ω : Set (Space n)} {p : ℝ≥0}
    (u : W1pData Ω p) (α : ℝ≥0) : Type where
  representative : Space n → ℝ
  agreesOnDomain : ∀ᵐ x ∂volume.restrict Ω, representative x = u.function x
  embeddingConstant : ℝ≥0
  holderOnClosure :
    HolderOnWith
      (embeddingConstant *
        (eLpNorm u.function (p : ℝ≥0∞) (volume.restrict Ω) +
          eLpNorm u.weakGradient (p : ℝ≥0∞) (volume.restrict Ω))).toNNReal
      α representative (closure Ω)
  valueBound :
    ∀ x ∈ closure Ω,
      ‖representative x‖₊ ≤
        embeddingConstant *
          (eLpNorm u.function (p : ℝ≥0∞) (volume.restrict Ω) +
            eLpNorm u.weakGradient (p : ℝ≥0∞) (volume.restrict Ω)).toNNReal

/--
Supercritical first-order Morrey-Sobolev embedding on bounded extension domains.
The equality fixes the exponent `α = 1 - n / p`; `p > n` excludes the critical
and subcritical cases.
-/
def Statement : Prop :=
  ∀ (n : ℕ) (_hn : 1 ≤ n) (Ω : Set (Space n)),
    MeasurableSet Ω → Bornology.IsBounded Ω →
      ∀ (p α : ℝ≥0), (n : ℝ) < p → (α : ℝ) = 1 - (n : ℝ) / p →
        ∀ u : W1pData Ω p, ExtensionData u →
          Nonempty (HolderRepresentative u α)

theorem statement_iff_expanded :
    Statement ↔
      ∀ (n : ℕ) (_hn : 1 ≤ n) (Ω : Set (Space n)),
        MeasurableSet Ω → Bornology.IsBounded Ω →
          ∀ (p α : ℝ≥0), (n : ℝ) < p → (α : ℝ) = 1 - (n : ℝ) / p →
            ∀ u : W1pData Ω p, ExtensionData u →
              Nonempty (HolderRepresentative u α) :=
  Iff.rfl

-- Structural mutation checks: these altered propositions are not definitionally
-- equal to the canonical root.
example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ (n : ℕ) (_hn : 1 ≤ n) (Ω : Set (Space n)),
        MeasurableSet Ω → Bornology.IsBounded Ω →
          ∀ (p α : ℝ≥0), ∀ u : W1pData Ω p, ExtensionData u →
            Nonempty (HolderRepresentative u α))
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ (n : ℕ) (_hn : 1 ≤ n) (Ω : Set (Space n)),
        MeasurableSet Ω → Bornology.IsBounded Ω →
          ∀ (p α : ℝ≥0), (n : ℝ) ≤ p → (α : ℝ) = 1 - (n : ℝ) / p →
            ∀ u : W1pData Ω p, ExtensionData u →
              Nonempty (HolderRepresentative u α))
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ (n : ℕ) (_hn : 1 ≤ n) (Ω : Set (Space n)),
        MeasurableSet Ω → Bornology.IsBounded Ω →
          ∀ (p α : ℝ≥0), (n : ℝ) < p → (α : ℝ) = 1 - (n : ℝ) / p →
            ∀ u : W1pData Ω p, ExtensionData u →
              Nonempty (HolderRepresentative u α) ∧ Ω.Nonempty)
  trivial

#check Statement
#print Statement

end Stage1Rev56.THMM1237
