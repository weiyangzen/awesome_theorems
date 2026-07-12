import Mathlib.ModelTheory.Satisfiability

open Set

namespace Stage1Instances.THM_M_0651

open FirstOrder
open FirstOrder.Language

universe u v w

variable {L : Language.{u, v}} (T : L.Theory) {α : Type w}

/-- A partial type over `T`: every finite subset is jointly realizable with `T`. -/
def IsPartialType (p : Set (L.Formula α)) : Prop :=
  ((L.lhomWithConstants α).onTheory T ∪ Formula.equivSentence '' p).IsFinitelySatisfiable

/-- `φ` isolates `p` over `T`: it is consistent with `T` and entails every member of `p`. -/
def Isolates (φ : L.Formula α) (p : Set (L.Formula α)) : Prop :=
  ((L.lhomWithConstants α).onTheory T ∪ {Formula.equivSentence φ}).IsSatisfiable ∧
    ∀ ψ ∈ p, T ⊨ᵇ φ.imp ψ

/-- A partial type is nonprincipal over `T` when no formula isolates it. -/
def IsNonprincipal (p : Set (L.Formula α)) : Prop :=
  ∀ φ, ¬Isolates T φ p

/-- A structure omits `p` when no tuple realizes every formula in `p`. -/
def Omits (M : Type*) [L.Structure M] (p : Set (L.Formula α)) : Prop :=
  ∀ a : α → M, ∃ φ ∈ p, ¬φ.Realize a

/-- Checked transport to the usual "there is no realizing tuple" formulation. -/
theorem omits_iff_no_realizing_tuple (M : Type*) [L.Structure M]
    (p : Set (L.Formula α)) :
    Omits M p ↔ ¬∃ a : α → M, ∀ φ ∈ p, φ.Realize a := by
  simp only [Omits, not_exists]
  apply forall_congr'
  intro a
  push Not
  rfl

/-- The simultaneous countable omitting types theorem, in fixed finite arity.

This is the canonical target only. Its proof is intentionally deferred to the proof phase. -/
def OmittingTypesTarget : Prop :=
  ∀ (L : Language.{u, v})
    [∀ n, Countable (L.Functions n)] [∀ n, Countable (L.Relations n)]
    (T : L.Theory) (arity : ℕ → ℕ)
    (p : (i : ℕ) → Set (L.Formula (Fin (arity i)))),
    T.IsSatisfiable →
    (∀ i, IsPartialType T (p i)) →
    (∀ i, IsNonprincipal T (p i)) →
    ∃ M : FirstOrder.Language.Theory.ModelType.{u, v, max u v} T,
      Countable M ∧ ∀ i, Omits M (p i)

#check OmittingTypesTarget

namespace MutationProbes

/-- Rejected mutation: drops the nonprincipality premise. -/
def WithoutNonprincipality : Prop :=
  ∀ (L : Language.{u, v})
    [∀ n, Countable (L.Functions n)] [∀ n, Countable (L.Relations n)]
    (T : L.Theory) (arity : ℕ → ℕ)
    (p : (i : ℕ) → Set (L.Formula (Fin (arity i)))),
    T.IsSatisfiable → (∀ i, IsPartialType T (p i)) →
    ∃ M : FirstOrder.Language.Theory.ModelType.{u, v, max u v} T,
      Countable M ∧ ∀ i, Omits M (p i)

/-- Rejected mutation: asks only that one chosen tuple fail to realize each type. -/
def OneTuplePerType : Prop :=
  ∀ (L : Language.{u, v})
    [∀ n, Countable (L.Functions n)] [∀ n, Countable (L.Relations n)]
    (T : L.Theory) (arity : ℕ → ℕ)
    (p : (i : ℕ) → Set (L.Formula (Fin (arity i)))),
    T.IsSatisfiable → (∀ i, IsPartialType T (p i)) →
    (∀ i, IsNonprincipal T (p i)) →
    ∃ M : FirstOrder.Language.Theory.ModelType.{u, v, max u v} T,
      Countable M ∧ ∀ i, ∃ a : Fin (arity i) → M, ∃ φ ∈ p i, ¬φ.Realize a

#check WithoutNonprincipality
#check OneTuplePerType

end MutationProbes

end Stage1Instances.THM_M_0651

set_option pp.explicit true in
#print Stage1Instances.THM_M_0651.OmittingTypesTarget
