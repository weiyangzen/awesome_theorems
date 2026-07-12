import «Statement»

/-!
# THM-M-0696 obligation interfaces

These declarations freeze the proof architecture.  Only the final composition from a
countermodel lemma to the canonical completeness target is proved here; the countermodel
lemma and its supporting interfaces remain open obligations.
-/

namespace Stage1Instances.THM_M_0696

universe u

def Neg {Atom : Type u} (phi : Formula Atom) : Formula Atom :=
  .imp phi .falsum

def Consistent {Atom : Type u} (Gamma : Set (Formula Atom)) : Prop :=
  ¬ Derives Gamma .falsum

def DeductivelyClosed {Atom : Type u} (Gamma : Set (Formula Atom)) : Prop :=
  ∀ {phi}, Derives Gamma phi → phi ∈ Gamma

def SyntacticallyComplete {Atom : Type u} (Gamma : Set (Formula Atom)) : Prop :=
  ∀ phi, phi ∈ Gamma ∨ Neg phi ∈ Gamma

def MaximalConsistent {Atom : Type u} (Gamma : Set (Formula Atom)) : Prop :=
  Consistent Gamma ∧ DeductivelyClosed Gamma ∧ SyntacticallyComplete Gamma

noncomputable def canonicalValuation {Atom : Type u} (Gamma : Set (Formula Atom)) : Atom → Bool :=
  by
    classical
    exact fun atom => if Derives Gamma (.atom atom) then true else false

/-- The deduction theorem needed to turn failure of derivability into a consistent seed. -/
def DeductionTheoremTarget : Prop :=
  ∀ (Atom : Type u) (Gamma : Set (Formula Atom)) (phi psi : Formula Atom),
    Derives (Set.insert phi Gamma) psi ↔ Derives Gamma (.imp phi psi)

/-- Nonderivability of `phi` makes `Gamma` extended by `¬phi` consistent. -/
def SeedConsistencyTarget : Prop :=
  ∀ (Atom : Type u) (Gamma : Set (Formula Atom)) (phi : Formula Atom),
    ¬ Derives Gamma phi → Consistent (Set.insert (Neg phi) Gamma)

/-- Lindenbaum extension, with no enumeration or decidability assumption on the atom type. -/
def LindenbaumTarget : Prop :=
  ∀ (Atom : Type u) (Gamma : Set (Formula Atom)), Consistent Gamma →
    ∃ Delta : Set (Formula Atom), Gamma ⊆ Delta ∧ MaximalConsistent Delta

/-- Formula-induction truth lemma for the canonical valuation. -/
def TruthLemmaTarget : Prop :=
  ∀ (Atom : Type u) (Delta : Set (Formula Atom)), MaximalConsistent Delta →
    ∀ phi, Formula.eval (canonicalValuation Delta) phi = true ↔ phi ∈ Delta

/-- The central semantic contrapositive package. -/
def CountermodelTarget : Prop :=
  ∀ (Atom : Type u) (Gamma : Set (Formula Atom)) (phi : Formula Atom),
    ¬ Derives Gamma phi →
      ∃ valuation : Atom → Bool,
        Satisfies valuation Gamma ∧ Formula.eval valuation phi = false

/-- Checked child-to-root composition.  This consumes the exact countermodel package. -/
theorem completeness_of_countermodel (hCountermodel : CountermodelTarget.{u}) :
    PropositionalCompletenessTarget.{u} := by
  intro Atom Gamma phi hSemantic
  by_contra hNotDerivable
  obtain ⟨valuation, hGamma, hFalse⟩ := hCountermodel Atom Gamma phi hNotDerivable
  have hTrue := hSemantic valuation hGamma
  simp [hFalse] at hTrue

#check DeductionTheoremTarget
#check SeedConsistencyTarget
#check LindenbaumTarget
#check TruthLemmaTarget
#check CountermodelTarget
#print axioms completeness_of_countermodel

end Stage1Instances.THM_M_0696
