import Statement

/-!
# THM-M-1200 conditional obligation composition

The explicit `NonzeroTracePackage` premise is the open bump-function subtree. This
file validates its exact child-to-root interface; it does not construct that package.
-/

namespace Stage1Instances.THM_M_1200

open MeasureTheory

/-- The exact output required from the open smooth-test construction subtree. -/
def NonzeroTracePackage : Prop :=
  ∀ s : Real, ∃ phi : Real × Real → Real,
    ContDiff Real ⊤ phi ∧ HasCompactSupport phi ∧
      (∫ t : Real, phi (t, s * t)) ≠ 0

/-- Checked composition from the open construction package to the frozen root. -/
theorem rankineHugoniotTarget_of_nonzeroTracePackage
    (testPackage : NonzeroTracePackage) : RankineHugoniotTarget := by
  intro f uL uR s
  constructor
  · intro vanishes
    obtain ⟨phi, smooth, compact, integral_ne⟩ := testPackage s
    have product_zero := vanishes phi smooth compact
    have coefficient_zero : jumpCoefficient f uL uR s = 0 := by
      simpa only [interfaceDefect] using (mul_eq_zero.mp product_zero).resolve_right integral_ne
    dsimp only [jumpCoefficient] at coefficient_zero
    linarith
  · intro jumpLaw phi smooth compact
    dsimp only [interfaceDefect, jumpCoefficient]
    have coefficient_zero : f uR - f uL - s * (uR - uL) = 0 := by
      linarith
    rw [coefficient_zero, zero_mul]

#print axioms rankineHugoniotTarget_of_nonzeroTracePackage

end Stage1Instances.THM_M_1200
