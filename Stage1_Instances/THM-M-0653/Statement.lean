import Mathlib.ModelTheory.Semantics

/-!
The exact statement surface for the one-relation form of Beth definability.
The distinguished relation has arity `n`; `PLift (k = n)` makes the added
language contain one relation symbol at precisely that arity and no functions.
-/

namespace Stage1.THM_M_0653

open FirstOrder FirstOrder.Language FirstOrder.Language.Structure

universe u v w

/-- The language containing only one `n`-ary relation symbol. -/
def OneRel (n : ℕ) : Language :=
  { Functions := fun _ => Empty
    Relations := fun k => PLift (k = n) }

/-- The unique added `n`-ary relation symbol. -/
def newRel (L : Language) (n : ℕ) : (L.sum (OneRel n)).Relations n :=
  Sum.inr ⟨rfl⟩

abbrev Expanded (L : Language) (n : ℕ) := L.sum (OneRel n)

/-- Two structures on the same carrier have literally the same base-language reduct. -/
def SameReduct (L : Language) (n : ℕ) (M : Type w)
    (s₁ s₂ : (Expanded L n).Structure M) : Prop :=
  @LHom.reduct L (Expanded L n) (LHom.sumInl : L →ᴸ Expanded L n) M s₁ =
    @LHom.reduct L (Expanded L n) (LHom.sumInl : L →ᴸ Expanded L n) M s₂

/-- `T` uniquely determines the added relation on every fixed base reduct. -/
def ImplicitlyDefines (L : Language) (n : ℕ) (T : (Expanded L n).Theory) : Prop :=
  ∀ (M : Type w) (_ : Nonempty M)
    (s₁ s₂ : (Expanded L n).Structure M),
    @Theory.Model (Expanded L n) M s₁ T →
    @Theory.Model (Expanded L n) M s₂ T →
    SameReduct L n M s₁ s₂ →
    ∀ x : Fin n → M,
      @RelMap (Expanded L n) M s₁ n (newRel L n) x ↔
        @RelMap (Expanded L n) M s₂ n (newRel L n) x

/-- One old-language formula uniformly defines the added relation in every model of `T`. -/
def ExplicitlyDefines (L : Language) (n : ℕ) (T : (Expanded L n).Theory) : Prop :=
  ∃ φ : L.Formula (Fin n),
    ∀ (M : Type w) (_ : Nonempty M) (s : (Expanded L n).Structure M),
      @Theory.Model (Expanded L n) M s T →
      ∀ x : Fin n → M,
        @RelMap (Expanded L n) M s n (newRel L n) x ↔
          @Formula.Realize L M
            (@LHom.reduct L (Expanded L n) (LHom.sumInl : L →ᴸ Expanded L n) M s)
            (Fin n) φ x

/-- Canonical rev-5.6 target: implicit and explicit definability are equivalent. -/
def BethDefinabilityTarget (L : Language.{u, v}) (n : ℕ)
    (T : (Expanded L n).Theory) : Prop :=
  (∀ (M : Type w) (_ : Nonempty M)
      (s₁ s₂ : (Expanded L n).Structure M),
      @Theory.Model (Expanded L n) M s₁ T →
      @Theory.Model (Expanded L n) M s₂ T →
      SameReduct L n M s₁ s₂ →
      ∀ x : Fin n → M,
        @RelMap (Expanded L n) M s₁ n (newRel L n) x ↔
          @RelMap (Expanded L n) M s₂ n (newRel L n) x) ↔
    ∃ φ : L.Formula (Fin n),
      ∀ (M : Type w) (_ : Nonempty M) (s : (Expanded L n).Structure M),
        @Theory.Model (Expanded L n) M s T →
        ∀ x : Fin n → M,
          @RelMap (Expanded L n) M s n (newRel L n) x ↔
            @Formula.Realize L M
              (@LHom.reduct L (Expanded L n) (LHom.sumInl : L →ᴸ Expanded L n) M s)
              (Fin n) φ x

#check BethDefinabilityTarget

end Stage1.THM_M_0653
