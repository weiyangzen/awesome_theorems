import Statement

/-!
# THM-M-0338 typed obligation boundary

This module kernel-checks only the logical composition chosen by the frozen
architecture.  `KadisonSingerComponents` is an explicit open premise; neither
existence nor uniqueness of extensions is claimed here.
-/

namespace Stage1.THM_M_0338

open scoped ComplexOrder

universe u

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- The existence half of the exact extension conclusion. -/
def ExtensionExists (diagonal : StarSubalgebra ℂ (Operators H))
    (φ : State diagonal) : Prop :=
  ∃ extension : State (Operators H), ∀ d : diagonal, extension d = φ d

/-- The at-most-one half, among all state extensions rather than only pure ones. -/
def ExtensionAtMostOne (diagonal : StarSubalgebra ℂ (Operators H))
    (φ : State diagonal) : Prop :=
  ∀ extension₁ extension₂ : State (Operators H),
    (∀ d : diagonal, extension₁ d = φ d) →
    (∀ d : diagonal, extension₂ d = φ d) → extension₁ = extension₂

/-- Package of the two root-relevant open proof interfaces.  The basis and
diagonal hypotheses are retained verbatim to prevent a broadened transport. -/
def KadisonSingerComponents : Prop :=
  ∀ (H : Type u) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (basis : HilbertBasis ℕ ℂ H) (diagonal : StarSubalgebra ℂ (Operators H)),
    (∀ T : Operators H,
      T ∈ diagonal ↔ ∀ i j : ℕ, i ≠ j → inner ℂ (basis i) (T (basis j)) = 0) →
    ∀ φ : State diagonal, IsPure φ →
      ExtensionExists diagonal φ ∧ ExtensionAtMostOne diagonal φ

/-- Checked child-to-parent composition.  Its premise remains the open proof
package and therefore this theorem gives no Kadison-Singer closure credit. -/
theorem root_of_components (components : KadisonSingerComponents.{u}) :
    KadisonSingerStatement.{u} := by
  intro H _ _ _ basis diagonal hdiagonal φ hpure
  obtain ⟨⟨extension, hextension⟩, hunique⟩ :=
    components H basis diagonal hdiagonal φ hpure
  refine ⟨extension, hextension, ?_⟩
  intro other hother
  exact hunique other extension hother hextension

#print axioms root_of_components

end Stage1.THM_M_0338
