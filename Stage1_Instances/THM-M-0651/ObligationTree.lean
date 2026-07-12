import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0651: obligation-tree composition probe

The substantive construction and avoidance interfaces are explicit premises.
This checks their types and their composition into the frozen target without
claiming that either interface has been discharged.
-/

open Set

namespace Stage1Instances.THM_M_0651.ObligationTree

open FirstOrder FirstOrder.Language

universe u v w

variable {L : Language.{u, v}} (T : L.Theory) {alpha : Type w}

def IsPartialType (p : Set (L.Formula alpha)) : Prop :=
  ((L.lhomWithConstants alpha).onTheory T ∪ Formula.equivSentence '' p).IsFinitelySatisfiable

def Isolates (phi : L.Formula alpha) (p : Set (L.Formula alpha)) : Prop :=
  ((L.lhomWithConstants alpha).onTheory T ∪ {Formula.equivSentence phi}).IsSatisfiable ∧
    ∀ psi ∈ p, T ⊨ᵇ phi.imp psi

def IsNonprincipal (p : Set (L.Formula alpha)) : Prop :=
  ∀ phi, ¬Isolates T phi p

def Omits (M : Type*) [L.Structure M] (p : Set (L.Formula alpha)) : Prop :=
  ∀ a : alpha → M, ∃ phi ∈ p, ¬phi.Realize a

def Root : Prop :=
  ∀ (L : Language.{u, v})
    [∀ n, Countable (L.Functions n)] [∀ n, Countable (L.Relations n)]
    (T : L.Theory) (arity : Nat → Nat)
    (p : (i : Nat) → Set (L.Formula (Fin (arity i)))),
    T.IsSatisfiable →
    (∀ i, IsPartialType T (p i)) →
    (∀ i, IsNonprincipal T (p i)) →
    ∃ M : Theory.ModelType.{u, v, max u v} T,
      Countable M ∧ ∀ i, Omits M (p i)

/-- Output of the countable Henkin construction before omission is proved. -/
structure Candidate (L : Language.{u, v}) (T : L.Theory) where
  model : Theory.ModelType.{u, v, max u v} T
  countable_model : Countable model

def ConstructionInterface : Prop :=
  ∀ (L : Language.{u, v})
    [∀ n, Countable (L.Functions n)] [∀ n, Countable (L.Relations n)]
    (T : L.Theory) (arity : Nat → Nat)
    (p : (i : Nat) → Set (L.Formula (Fin (arity i)))),
    T.IsSatisfiable →
    (∀ i, IsPartialType T (p i)) →
    (∀ i, IsNonprincipal T (p i)) →
    Nonempty (Candidate L T)

def AvoidanceInterface : Prop :=
  ∀ (L : Language.{u, v}) (T : L.Theory) (arity : Nat → Nat)
    (p : (i : Nat) → Set (L.Formula (Fin (arity i)))),
    (∀ i, IsPartialType T (p i)) →
    (∀ i, IsNonprincipal T (p i)) →
    ∀ c : Candidate L T, ∀ i, Omits c.model (p i)

/-- Checked child-to-parent composition; the two open mathematical interfaces
remain premises for the proof phase. -/
theorem root_compose
    (construct : ConstructionInterface.{u, v})
    (avoid : AvoidanceInterface.{u, v}) : Root.{u, v} := by
  intro L _ _ T arity p hsat hpartial hnonprincipal
  obtain ⟨c⟩ := construct L T arity p hsat hpartial hnonprincipal
  exact ⟨c.model, c.countable_model, avoid L T arity p hpartial hnonprincipal c⟩

#check Root
#check ConstructionInterface
#check AvoidanceInterface
#print axioms root_compose

end Stage1Instances.THM_M_0651.ObligationTree
