import «Statement»

/-!
# THM-M-1237 obligation composition

This harness checks only the exact child-to-root assembly. The analytic
Morrey estimate, representative construction, and value estimate remain
explicit premises and therefore remain open obligations.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal NNReal Topology

namespace Stage1Rev56.THMM1237.ObligationTree

open Stage1Rev56.THMM1237

def RepresentativeFamily : Prop :=
  ∀ (n : ℕ) (_hn : 1 ≤ n) (Ω : Set (Space n)),
    MeasurableSet Ω → Bornology.IsBounded Ω →
      ∀ (p α : ℝ≥0), (n : ℝ) < p → (α : ℝ) = 1 - (n : ℝ) / p →
        ∀ u : W1pData Ω p, ExtensionData u →
          ∃ representative : Space n → ℝ,
            ∀ᵐ x ∂volume.restrict Ω, representative x = u.function x

def HolderEstimateFamily : Prop :=
  ∀ (n : ℕ) (hn : 1 ≤ n) (Ω : Set (Space n))
    (hΩm : MeasurableSet Ω) (hΩb : Bornology.IsBounded Ω)
    (p α : ℝ≥0) (hp : (n : ℝ) < p) (hα : (α : ℝ) = 1 - (n : ℝ) / p)
    (u : W1pData Ω p) (ext : ExtensionData u),
    ∀ representative : Space n → ℝ,
      (∀ᵐ x ∂volume.restrict Ω, representative x = u.function x) → ∃ C : ℝ≥0,
      HolderOnWith
        (C * (eLpNorm u.function (p : ℝ≥0∞) (volume.restrict Ω) +
          eLpNorm u.weakGradient (p : ℝ≥0∞) (volume.restrict Ω))).toNNReal
        α representative (closure Ω)

def ValueEstimateFamily : Prop :=
  ∀ (n : ℕ) (hn : 1 ≤ n) (Ω : Set (Space n))
    (hΩm : MeasurableSet Ω) (hΩb : Bornology.IsBounded Ω)
    (p α : ℝ≥0) (hp : (n : ℝ) < p) (hα : (α : ℝ) = 1 - (n : ℝ) / p)
    (u : W1pData Ω p) (ext : ExtensionData u),
    ∀ (representative : Space n → ℝ),
      (∀ᵐ x ∂volume.restrict Ω, representative x = u.function x) →
      ∀ C : ℝ≥0, ∀ x ∈ closure Ω, ‖representative x‖₊ ≤
        C * (eLpNorm u.function (p : ℝ≥0∞) (volume.restrict Ω) +
          eLpNorm u.weakGradient (p : ℝ≥0∞) (volume.restrict Ω)).toNNReal

/-- Exact terminal composition. Each analytic child premise is consumed. -/
theorem root_compose
    (representative : RepresentativeFamily)
    (holder : HolderEstimateFamily)
    (value : ValueEstimateFamily) : Statement := by
  intro n hn Ω hΩm hΩb p α hp hα u ext
  obtain ⟨f, hf⟩ := representative n hn Ω hΩm hΩb p α hp hα u ext
  obtain ⟨C, hC⟩ := holder n hn Ω hΩm hΩb p α hp hα u ext f hf
  exact ⟨{
    representative := f
    agreesOnDomain := hf
    embeddingConstant := C
    holderOnClosure := hC
    valueBound := value n hn Ω hΩm hΩb p α hp hα u ext f hf C
  }⟩

#check root_compose
#print axioms root_compose

end Stage1Rev56.THMM1237.ObligationTree
