import Statement

/-!
# THM-M-0645: counterexample to the frozen target

The frozen calculus specializes sentence proofs to the free-variable type `Empty`, while its
universal-introduction rule requires an inhabitant of that type.  This module gives the resulting
kernel-checked counterexample: the valid sentence `forall x, x = x` cannot be derived.
-/

namespace Stage1Instances.THM_M_0645

open FirstOrder
open FirstOrder.Language

/-- A syntactic interpretation used only to prove nonderivability.  Equality and relations are
true, implication has its usual meaning, and every universal formula is false. -/
def proofInvariant {L : Language} {alpha : Type*} {n : Nat} :
    L.BoundedFormula alpha n -> Prop
  | .falsum => False
  | .equal _ _ => True
  | .rel _ _ => True
  | .imp phi psi => proofInvariant phi -> proofInvariant psi
  | .all _ => False

theorem proofInvariant_subst {L : Language} {alpha beta : Type*} {n : Nat}
    (phi : L.BoundedFormula alpha n) (sigma : alpha -> L.Term beta) :
    proofInvariant (phi.subst sigma) <-> proofInvariant phi := by
  induction phi with
  | falsum => rfl
  | equal => rfl
  | rel => rfl
  | imp phi psi ihPhi ihPsi =>
      simp only [BoundedFormula.subst, BoundedFormula.mapTermRel, proofInvariant]
      exact imp_congr ihPhi ihPsi
  | all phi ih => rfl

theorem proofInvariant_substituteFree {L : Language} {alpha : Type*}
    (theta : L.Formula (alpha ⊕ Unit)) (t : L.Term alpha) :
    proofInvariant (substituteFree theta t) <-> proofInvariant theta :=
  proofInvariant_subst theta (Sum.elim Term.var (fun _ => t))

/-- Every derivation whose free-variable type is empty satisfies `proofInvariant`.  The
`allIntro` case is impossible because its eigenvariable would have type `Empty`. -/
theorem proofInvariant_of_derivation {L : Language} {Gamma : List (L.Sentence)}
    {phi : L.Sentence} (hGamma : forall psi, psi ∈ Gamma -> proofInvariant psi)
    (derivation : Derivation L (alpha := Empty) Gamma phi) : proofInvariant phi := by
  induction derivation with
  | hyp hmem => exact hGamma _ hmem
  | falsumElim _ ih => exact False.elim (ih hGamma)
  | impIntro derivation ih =>
      exact fun hPhi => ih (fun psi hmem => by
        simp only [List.mem_cons] at hmem
        exact hmem.elim (fun hEq => hEq ▸ hPhi) (hGamma psi))
  | impElim _ _ ihImp ihPhi => exact ihImp hGamma (ihPhi hGamma)
  | classical =>
      simp only [proofInvariant]
      tauto
  | allIntro x => exact Empty.elim x
  | allElim t _ ih =>
      exact False.elim (ih hGamma)
  | equalityRefl => trivial
  | equalityElim theta s t _ _ _ ihTheta =>
      exact (proofInvariant_substituteFree theta t).mpr
        ((proofInvariant_substituteFree theta s).mp (ihTheta hGamma))

/-- A universe-polymorphic symbol-free language used to instantiate the target's exact binders. -/
def emptyLanguage : Language.{u, v} where
  Functions _ := ULift.{u} Empty
  Relations _ := ULift.{v} Empty

/-- The closed symbol-free sentence `forall x, x = x`. -/
def reflexivitySentence : emptyLanguage.Sentence :=
  (BoundedFormula.equal (Term.var (Sum.inr 0)) (Term.var (Sum.inr 0)) :
    emptyLanguage.BoundedFormula Empty 1).all

theorem reflexivitySentence_valid : Valid reflexivitySentence := by
  intro M _ _
  simp [reflexivitySentence, Sentence.Realize, Formula.Realize,
    BoundedFormula.Realize, Term.realize]

theorem reflexivitySentence_not_provable : Not (Provable reflexivitySentence) := by
  rintro ⟨derivation⟩
  exact proofInvariant_of_derivation (by simp) derivation

/-- The exact frozen `CompletenessTarget` is false for the calculus in `Statement.lean`. -/
theorem not_completenessTarget : Not CompletenessTarget := by
  intro completeness
  exact reflexivitySentence_not_provable
    (completeness emptyLanguage reflexivitySentence reflexivitySentence_valid)

#print axioms proofInvariant_of_derivation
#print axioms reflexivitySentence_valid
#print axioms reflexivitySentence_not_provable
#print axioms not_completenessTarget

end Stage1Instances.THM_M_0645
