import Init

/-!
# THM-M-0392 obligation composition

This module checks only the conditional composition of the frozen architecture.
It does not assert a Siegel theorem or an integral-point finiteness result.
-/

namespace Stage1Instances.THMM0392.ObligationTree

def IsFinite (α : Type) : Prop :=
  ∃ n : Nat, ∃ encode : α → Fin n, Function.Injective encode

def Solutions (k : Int) :=
  {p : Int × Int // p.2 ^ 2 = p.1 ^ 3 + k}

def Root : Prop :=
  ∀ k : Int, k ≠ 0 → IsFinite (Solutions k)

variable (IntegralPoints : Int → Type)
variable (CurveEligible : Int → Prop)

def EligibilityBridge : Prop :=
  ∀ k : Int, k ≠ 0 → CurveEligible k

def IntegralPointFiniteness : Prop :=
  ∀ k : Int, CurveEligible k → IsFinite (IntegralPoints k)

def CoordinateEmbedding : Type :=
  ∀ k : Int, Solutions k → IntegralPoints k

def CoordinateEmbeddingInjective (embed : CoordinateEmbedding IntegralPoints) : Prop :=
  ∀ k : Int, Function.Injective (embed k)

theorem finite_of_injective
    {α β : Type} (f : α → β) (hf : Function.Injective f) (hβ : IsFinite β) :
    IsFinite α := by
  rcases hβ with ⟨n, encode, hencode⟩
  exact ⟨n, encode ∘ f, hencode.comp hf⟩

/-- Conditional certificate: the curve bridge, finiteness bridge, and coordinate
embedding are all explicit premises rather than hidden theorem claims. -/
theorem root_compose
    (eligible : EligibilityBridge CurveEligible)
    (finitePoints : IntegralPointFiniteness IntegralPoints CurveEligible)
    (embed : CoordinateEmbedding IntegralPoints)
    (embed_injective : CoordinateEmbeddingInjective IntegralPoints embed) : Root := by
  intro k hk
  exact finite_of_injective (embed k) (embed_injective k) (finitePoints k (eligible k hk))

theorem root_exact_type :
    Root =
      (∀ k : Int, k ≠ 0 →
        IsFinite {p : Int × Int // p.2 ^ 2 = p.1 ^ 3 + k}) :=
  rfl

#print root_compose
#print axioms root_compose

end Stage1Instances.THMM0392.ObligationTree
