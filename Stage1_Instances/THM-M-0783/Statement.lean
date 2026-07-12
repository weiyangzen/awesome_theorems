import Mathlib.SetTheory.Cardinal.Continuum

/-!
# THM-M-0783: Martin's axiom

This module freezes Martin's axiom as a proposition in Lean. It does not assume
the axiom and does not provide a proof of it.
-/

namespace Stage1Instances.THM_M_0783

open Cardinal

universe u

/-- Two forcing conditions are compatible when they have a common stronger
extension. Here `q <= p` means that `q` is stronger than `p`. -/
def Compatible {P : Type u} [Preorder P] (p q : P) : Prop :=
  ∃ r : P, r ≤ p ∧ r ≤ q

/-- A subset of a forcing order is an antichain when distinct members are
incompatible. -/
def IsForcingAntichain {P : Type u} [Preorder P] (A : Set P) : Prop :=
  ∀ p ∈ A, ∀ q ∈ A, p ≠ q → ¬ Compatible p q

/-- The countable chain condition: every forcing antichain is countable. -/
def HasCCC (P : Type u) [Preorder P] : Prop :=
  ∀ A : Set P, IsForcingAntichain A → A.Countable

/-- `D` is dense when every condition has a stronger member of `D`. -/
def IsForcingDense {P : Type u} [Preorder P] (D : Set P) : Prop :=
  ∀ p : P, ∃ q : P, q ∈ D ∧ q ≤ p

/-- A forcing filter, using the convention that smaller conditions are
stronger: it is nonempty, upward closed, and downward directed. -/
def IsForcingFilter {P : Type u} [Preorder P] (G : Set P) : Prop :=
  G.Nonempty ∧
    (∀ {p q : P}, p ∈ G → p ≤ q → q ∈ G) ∧
    (∀ {p q : P}, p ∈ G → q ∈ G →
      ∃ r : P, r ∈ G ∧ r ≤ p ∧ r ≤ q)

/-- `MA(kappa)`: every family of at most `kappa` dense subsets of a nonempty
ccc partial order is met by a filter. -/
def MartinsAxiomAt (kappa : Cardinal.{u}) : Prop :=
  ∀ (P : Type u) [PartialOrder P] [Nonempty P], HasCCC P →
    ∀ (I : Type u) (D : I → Set P), #I ≤ kappa →
      (∀ i : I, IsForcingDense (D i)) →
        ∃ G : Set P, IsForcingFilter G ∧ ∀ i : I, (G ∩ D i).Nonempty

/-- Canonical target: `MA(kappa)` holds for every cardinal strictly below the
continuum. This is a proposition recording the additional set-theoretic axiom,
not a theorem claimed to follow from Lean's foundations. -/
def MartinsAxiom : Prop :=
  ∀ kappa : Cardinal.{u}, kappa < 𝔠 → MartinsAxiomAt kappa

/-- Direct expansion of the selected canonical target. -/
def ExpandedMartinsAxiom : Prop :=
  ∀ kappa : Cardinal.{u}, kappa < 𝔠 →
    ∀ (P : Type u) [PartialOrder P] [Nonempty P], HasCCC P →
      ∀ (I : Type u) (D : I → Set P), #I ≤ kappa →
        (∀ i : I, IsForcingDense (D i)) →
          ∃ G : Set P, IsForcingFilter G ∧ ∀ i : I, (G ∩ D i).Nonempty

/-- Checked definitional transport to the fully expanded binder shape. -/
theorem martinsAxiom_iff_expanded :
    MartinsAxiom.{u} ↔ ExpandedMartinsAxiom.{u} := by
  rfl

-- Structural mutations are elaborated and distinguished by check_statement.py.
def mutationRemovedCCC : Prop :=
  ∀ kappa : Cardinal.{u}, kappa < 𝔠 →
    ∀ (P : Type u) [PartialOrder P] [Nonempty P],
      ∀ (I : Type u) (D : I → Set P), #I ≤ kappa →
        (∀ i : I, IsForcingDense (D i)) →
          ∃ G : Set P, IsForcingFilter G ∧ ∀ i : I, (G ∩ D i).Nonempty

def mutationChangedCardinalBound : Prop :=
  ∀ kappa : Cardinal.{u}, kappa ≤ 𝔠 → MartinsAxiomAt kappa

def mutationChangedBinderScope : Prop :=
  ∀ kappa : Cardinal.{u}, kappa < 𝔠 →
    ∀ (P : Type u) [PartialOrder P] [Nonempty P], HasCCC P →
      ∀ I : Type u, #I ≤ kappa →
        ∃ G : Set P, IsForcingFilter G ∧
          ∀ D : I → Set P, (∀ i : I, IsForcingDense (D i)) →
            ∀ i : I, (G ∩ D i).Nonempty

def mutationChangedDomain : Prop :=
  ∀ kappa : Cardinal.{u}, kappa < 𝔠 →
    ∀ (P : Type u) [Preorder P] [Nonempty P], HasCCC P →
      ∀ (I : Type u) (D : I → Set P), #I ≤ kappa →
        (∀ i : I, IsForcingDense (D i)) →
          ∃ G : Set P, IsForcingFilter G ∧ ∀ i : I, (G ∩ D i).Nonempty

/-- The empty dense-set family is met by the whole forcing order. -/
theorem empty_family_boundary (P : Type u) [PartialOrder P] [Nonempty P] :
    ∃ G : Set P, IsForcingFilter G ∧
      ∀ i : Empty, (G ∩ (Empty.elim i : Set P)).Nonempty := by
  let p : P := Classical.choice inferInstance
  refine ⟨Set.Ici p, ?_, ?_⟩
  · refine ⟨⟨p, le_rfl⟩, ?_, ?_⟩
    · intro q r hpq hqr
      exact hpq.trans hqr
    · intro q r hq hr
      exact ⟨p, le_rfl, hq, hr⟩
  · intro i
    exact i.elim

end Stage1Instances.THM_M_0783

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0783.MartinsAxiom
