import Proof
import Mathlib.Analysis.Complex.ReImTopology
import Mathlib.Analysis.Complex.Convex

/-!
# THM-M-1146 additional proof bodies

This module implements the construction-continuity and local branch-merge obligations needed before
the still-open analytic gluing step at the reflecting axis.
-/

namespace Stage1Instances.THM_M_1146

open Complex InnerProductSpace Metric Set Topology
open scoped ComplexConjugate

noncomputable section

/-- The odd reflection is continuous on the exact part of the closed upper half-plane supplied by
the frozen continuity hypothesis. -/
theorem oddReflection_continuousOn_nonnegative
    {V : Set ℂ} {u : ℂ → ℝ}
    (hu : ContinuousOn u (upperPart V ∪ reflectingPart V)) :
    ContinuousOn (oddReflection u) (V ∩ {z : ℂ | 0 ≤ z.im}) := by
  have hsubset : V ∩ {z : ℂ | 0 ≤ z.im} ⊆ upperPart V ∪ reflectingPart V := by
    rintro z ⟨hzV, hzim⟩
    change 0 ≤ z.im at hzim
    rcases eq_or_lt_of_le hzim with haxis | hpos
    · exact Or.inr ⟨hzV, haxis.symm⟩
    · exact Or.inl ⟨hzV, hpos⟩
  exact (hu.mono hsubset).congr fun z hz =>
    oddReflection_eq_of_nonnegative_imaginary u z (show 0 ≤ z.im from hz.2)

/-- The odd reflection is continuous on the closed lower half-plane by conjugating the exact
upper-side continuity set. -/
theorem oddReflection_continuousOn_nonpositive
    {V : Set ℂ} {u : ℂ → ℝ}
    (hsym : ∀ z, z ∈ V ↔ conj z ∈ V)
    (hu : ContinuousOn u (upperPart V ∪ reflectingPart V))
    (hzero : ∀ z ∈ reflectingPart V, u z = 0) :
    ContinuousOn (oddReflection u) (V ∩ {z : ℂ | z.im ≤ 0}) := by
  let g : ℂ → ℝ := fun z => -u (conj z)
  have hg : ContinuousOn g (V ∩ {z : ℂ | z.im ≤ 0}) := by
    apply ContinuousOn.neg
    apply hu.comp continuous_conj.continuousOn
    rintro z ⟨hzV, hzim⟩
    change z.im ≤ 0 at hzim
    rcases eq_or_lt_of_le hzim with haxis | hneg
    · apply Or.inr
      exact ⟨(hsym z).mp hzV, by simpa using haxis⟩
    · apply Or.inl
      exact ⟨(hsym z).mp hzV, by simpa using hneg⟩
  apply hg.congr
  rintro z ⟨hzV, hzim⟩
  change z.im ≤ 0 at hzim
  rcases eq_or_lt_of_le hzim with haxis | hneg
  · have hzreflecting : z ∈ reflectingPart V := ⟨hzV, haxis⟩
    have hczreflecting : conj z ∈ reflectingPart V := by
      exact ⟨(hsym z).mp hzV, by simpa using haxis⟩
    simp [oddReflection, haxis, hzero z hzreflecting, hzero (conj z) hczreflecting, g]
  · simp [oddReflection, not_le.mpr hneg, g]

/-- The reflected construction is continuous on all of the symmetric domain. -/
theorem oddReflection_continuousOn
    {V : Set ℂ} {u : ℂ → ℝ}
    (hsym : ∀ z, z ∈ V ↔ conj z ∈ V)
    (hu : ContinuousOn u (upperPart V ∪ reflectingPart V))
    (hzero : ∀ z ∈ reflectingPart V, u z = 0) :
    ContinuousOn (oddReflection u) V := by
  let g : ℂ → ℝ := fun z => -u (conj z)
  have hupper := oddReflection_continuousOn_nonnegative (V := V) hu
  have hlower : ContinuousOn g (V ∩ closure {z : ℂ | ¬ 0 ≤ z.im}) := by
    rw [show closure {z : ℂ | ¬ 0 ≤ z.im} = {z : ℂ | z.im ≤ 0} by
      simpa only [not_le] using Complex.closure_setOf_im_lt 0]
    apply ContinuousOn.neg
    apply hu.comp continuous_conj.continuousOn
    rintro z ⟨hzV, hzim⟩
    change z.im ≤ 0 at hzim
    rcases eq_or_lt_of_le hzim with haxis | hneg
    · exact Or.inr ⟨(hsym z).mp hzV, by simpa using haxis⟩
    · exact Or.inl ⟨(hsym z).mp hzV, by simpa using hneg⟩
  have hpiece : ContinuousOn (fun z => if 0 ≤ z.im then u z else g z) V := by
    apply ContinuousOn.if
    · intro z hz
      rw [Complex.frontier_setOf_le_im] at hz
      have hzreflecting : z ∈ reflectingPart V := ⟨hz.1, hz.2⟩
      have hczreflecting : conj z ∈ reflectingPart V :=
        ⟨(hsym z).mp hz.1, by simpa using hz.2⟩
      simp [g, hzero z hzreflecting, hzero (conj z) hczreflecting]
    · rw [show closure {z : ℂ | 0 ≤ z.im} = {z : ℂ | 0 ≤ z.im} by
        exact (isClosed_le continuous_const continuous_im).closure_eq]
      exact (hu.mono (by
        rintro z ⟨hzV, hzim⟩
        change 0 ≤ z.im at hzim
        rcases eq_or_lt_of_le hzim with haxis | hpos
        · exact Or.inr ⟨hzV, haxis.symm⟩
        · exact Or.inl ⟨hzV, hpos⟩))
    · exact hlower
  simpa [oddReflection, g] using hpiece

/-- Once the real-axis gluing body is supplied, the three pointwise branches merge into the exact
reflected-harmonic package. -/
theorem reflectedHarmonicPackage_of_axis
    (axis : ∀ (V : Set ℂ) (u : ℂ → ℝ),
      IsOpen V →
      (∀ z, z ∈ V ↔ conj z ∈ V) →
      HarmonicOnNhd u (upperPart V) →
      ContinuousOn u (upperPart V ∪ reflectingPart V) →
      (∀ z ∈ reflectingPart V, u z = 0) →
      ∀ z ∈ V, z.im = 0 → HarmonicAt (oddReflection u) z) :
    ReflectedHarmonicPackage := by
  intro V u hV hsym hu hcont hzero z hzV
  rcases lt_trichotomy z.im 0 with hneg | haxis | hpos
  · exact oddReflection_harmonicAt_of_mem_negative hsym hu hzV hneg
  · exact axis V u hV hsym hu hcont hzero z hzV haxis
  · exact oddReflection_harmonicAt_of_pos hpos (hu z ⟨hzV, hpos⟩)

#print axioms oddReflection_continuousOn_nonnegative
#print axioms oddReflection_continuousOn_nonpositive
#print axioms oddReflection_continuousOn
#print axioms reflectedHarmonicPackage_of_axis

end
end Stage1Instances.THM_M_1146
