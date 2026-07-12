import Mathlib.Analysis.Distribution.Distribution
import Mathlib.Analysis.Distribution.Support

/-!
# THM-M-1252: support and localization of a distribution

This module freezes the localization characterization selected by the intake.
It contains the target proposition, not a new proof of that proposition.
-/

noncomputable section

open Set TopologicalSpace
open scoped Distributions

namespace Stage1Instances.THM_M_1252

universe u

/-- The complement of the support of a real scalar distribution is the union
of all open sets on which the distribution vanishes. -/
def DistributionSupportLocalizationTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      (Distribution.dsupport T)ᶜ =
        ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsOpen U}

/-- Fully quantified expansion used to check that no restriction or support
condition is hidden by the canonical target name. -/
def ExpandedTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      (Distribution.dsupport T)ᶜ =
        ⋃₀ {U : Set E |
          (∀ φ : TestFunction Ω ℝ ⊤, tsupport φ ⊆ U → T φ = 0) ∧ IsOpen U}

/-- Checked transport from the named target to its test-function expansion. -/
theorem distributionSupportLocalizationTarget_iff_expandedTarget :
    DistributionSupportLocalizationTarget.{u} ↔ ExpandedTarget.{u} := by
  simp only [DistributionSupportLocalizationTarget, ExpandedTarget,
    Distribution.IsVanishingOn]

-- Separately elaborated structural mutations for statement review.
def mutationClosedZeroRegions : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      (Distribution.dsupport T)ᶜ =
        ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsClosed U}

def mutationSupportInsteadOfComplement : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      Distribution.dsupport T =
        ⋃₀ {U : Set E | Distribution.IsVanishingOn T U ∧ IsOpen U}

def mutationExistsZeroRegion : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
    (Ω : Opens E) (T : Distribution Ω ℝ ⊤),
      ∃ U : Set E, Distribution.IsVanishingOn T U ∧ IsOpen U ∧
        (Distribution.dsupport T)ᶜ = U

end Stage1Instances.THM_M_1252

set_option pp.explicit true in
#print Stage1Instances.THM_M_1252.DistributionSupportLocalizationTarget
