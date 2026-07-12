import Mathlib.ModelTheory.Semantics

/-!
# THM-M-0645: first-order completeness statement boundary

This module fixes a concrete classical natural-deduction calculus with equality and states weak
completeness for closed formulas. It intentionally supplies no proof of completeness.
-/

open FirstOrder
open FirstOrder.Language

namespace Stage1Instances.THM_M_0645

universe u v w

/-- Replace the distinguished free variable in a formula by a term. -/
def substituteFree {L : Language.{u, v}} {alpha : Type w}
    (phi : L.Formula (alpha ⊕ Unit)) (t : L.Term alpha) : L.Formula alpha :=
  phi.subst (Sum.elim Term.var (fun _ => t))

/-- Instantiate the sole exposed bound variable of a quantified formula. -/
def instantiate {L : Language.{u, v}} {alpha : Type w}
    (phi : L.BoundedFormula alpha 1) (t : L.Term alpha) : L.Formula alpha :=
  phi.toFormula.subst (Sum.elim Term.var (fun _ => t))

/-- Finite classical natural deductions for first-order logic with logical equality. -/
inductive Derivation (L : Language.{u, v}) {alpha : Type w} [DecidableEq alpha] :
    List (L.Formula alpha) -> L.Formula alpha -> Type (max u v w)
  | hyp {Gamma phi} : phi ∈ Gamma -> Derivation L Gamma phi
  | falsumElim {Gamma phi} : Derivation L Gamma ⊥ -> Derivation L Gamma phi
  | impIntro {Gamma phi psi} :
      Derivation L (phi :: Gamma) psi -> Derivation L Gamma (phi.imp psi)
  | impElim {Gamma phi psi} :
      Derivation L Gamma (phi.imp psi) -> Derivation L Gamma phi -> Derivation L Gamma psi
  | classical {Gamma} {phi : L.Formula alpha} : Derivation L Gamma (phi.not.not.imp phi)
  | allIntro {Gamma} {phi : L.BoundedFormula alpha 1} (x : alpha)
      (freshContext : forall (psi), psi ∈ Gamma -> x ∉ psi.freeVarFinset)
      (freshConclusion : x ∉ phi.all.freeVarFinset) :
      Derivation L Gamma (instantiate phi (Term.var x)) -> Derivation L Gamma phi.all
  | allElim {Gamma} {phi : L.BoundedFormula alpha 1} (t : L.Term alpha) :
      Derivation L Gamma phi.all -> Derivation L Gamma (instantiate phi t)
  | equalityRefl {Gamma} (t : L.Term alpha) : Derivation L Gamma (t.equal t)
  | equalityElim {Gamma} (theta : L.Formula (alpha ⊕ Unit)) (s t : L.Term alpha) :
      Derivation L Gamma (s.equal t) ->
      Derivation L Gamma (substituteFree theta s) ->
      Derivation L Gamma (substituteFree theta t)

/-- A sentence is valid when it holds in every nonempty structure for its language. -/
def Valid {L : Language.{u, v}} (phi : L.Sentence) : Prop :=
  forall (M : Type (max u v)), [Nonempty M] -> [L.Structure M] -> M ⊨ phi

/-- Provability from no assumptions in the fixed finite calculus. -/
def Provable {L : Language.{u, v}} (phi : L.Sentence) : Prop :=
  Nonempty (Derivation L (alpha := Empty) [] phi)

/-- Goedel completeness for classical first-order logic with equality, in weak validity form. -/
def CompletenessTarget : Prop :=
  forall (L : Language.{u, v}) (phi : L.Sentence), Valid phi -> Provable phi

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedValidity : Prop :=
  forall (L : Language.{u, v}) (phi : L.Sentence), Provable phi

def mutationAllowsEmptyDomains : Prop :=
  forall (L : Language.{u, v}) (phi : L.Sentence),
    (forall (M : Type (max u v)), [L.Structure M] -> M ⊨ phi) -> Provable phi

def mutationEmptyLanguageOnly : Prop :=
  forall (phi : Language.empty.Sentence), Valid phi -> Provable phi

def mutationChangedBinderScope : Prop :=
  forall (L : Language.{u, v}),
    (forall phi : L.Sentence, Valid phi) -> forall phi : L.Sentence, Provable phi

/-- The empty language remains included: `false implies false` has a direct empty-context proof. -/
def emptyLanguageBoundary :
    Derivation Language.empty (alpha := Empty) []
      ((⊥ : Language.empty.Sentence).imp ⊥) :=
  Derivation.impIntro (Derivation.hyp (by simp))

end Stage1Instances.THM_M_0645

set_option pp.explicit true in
#print Stage1Instances.THM_M_0645.CompletenessTarget
