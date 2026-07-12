import Statement

/-!
# THM-M-1141 conditional obligation composition

This module checks the final algebraic composition boundary selected by the
frozen architecture. The uniform comparison package remains an explicit
premise; no Harnack inequality proof is asserted here.
-/

open Set
open InnerProductSpace

namespace Stage1Instances.THM_M_1141

/-- Output expected from the local-ball estimate and the compact Harnack-chain
assembly. The same constant controls both orientations. -/
def UniformValueComparison : Prop :=
  ∀ (n : Nat) (Ω K : Set (Space n)),
    IsOpen Ω → IsConnected Ω → IsCompact K → K ⊆ Ω →
    ∃ A : Real, 1 ≤ A ∧
      ∀ (u : Space n → Real), HarmonicOnNhd u Ω →
        (∀ z ∈ Ω, 0 < u z) →
        ∀ x ∈ K, ∀ y ∈ K, u y ≤ A * u x ∧ u x ≤ A * u y

/-- Checked conversion of a symmetric multiplicative value comparison into
the canonical two-sided ratio formulation with a strictly larger constant. -/
theorem harnackInequality_of_uniformValueComparison
    (comparison : UniformValueComparison) : HarnackInequality := by
  intro n Ω K hΩopen hΩconnected hKcompact hKΩ
  obtain ⟨A, hA, hcompare⟩ :=
    comparison n Ω K hΩopen hΩconnected hKcompact hKΩ
  refine ⟨A + 1, by linarith, ?_⟩
  intro u hu hupos x hx y hy
  have hxΩ : x ∈ Ω := hKΩ hx
  have hyΩ : y ∈ Ω := hKΩ hy
  have hux : 0 < u x := hupos x hxΩ
  have huy : 0 < u y := hupos y hyΩ
  obtain ⟨hyx, hxy⟩ := hcompare u hu hupos x hx y hy
  constructor
  · rw [one_div]
    rw [le_div_iff₀ hux, inv_mul_eq_div]
    rw [div_le_iff₀ (by linarith : 0 < A + 1)]
    nlinarith
  · apply (div_le_iff₀ hux).2
    nlinarith

#print axioms harnackInequality_of_uniformValueComparison

end Stage1Instances.THM_M_1141
