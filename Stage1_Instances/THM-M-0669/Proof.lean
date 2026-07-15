import Statement
import Mathlib.ModelTheory.Algebra.Ring.FreeCommRing
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0669 proof-phase progress

This module discharges the pure-ring atomic and Boolean syntax branches and
implements formula recursion from an explicit one-variable elimination
package.  The package itself is the still-open algebraic Tarski step, so the
conditional terminal theorem below does not prove the canonical root.
-/

namespace Stage1.THM_M_0669

open FirstOrder FirstOrder.Language
open scoped FirstOrder

/-- A formula already known to be quantifier-free is its own checked
quantifier-free equivalent. -/
theorem qfEquivalent_of_isQF
    {alpha : Type} {n : Nat}
    {phi : Language.ring.BoundedFormula alpha n} (hphi : phi.IsQF) :
    exists psi : Language.ring.BoundedFormula alpha n,
      psi.IsQF ∧ phi ⇔[realClosedFieldTheory] psi := by
  exact ⟨phi, hphi, Language.Theory.Iff.refl phi⟩

/-- In the pure ring language every atomic formula is an equality of ring
terms; there are no relation-symbol cases.  The returned equality is also
quantifier-free. -/
theorem atomicEqualityNormalization
    {alpha : Type} {n : Nat}
    {phi : Language.ring.BoundedFormula alpha n} (hphi : phi.IsAtomic) :
    exists t₁ t₂ : Language.ring.Term (alpha ⊕ Fin n),
      phi = t₁.bdEqual t₂ ∧ phi.IsQF := by
  cases hphi with
  | equal t₁ t₂ =>
      exact ⟨t₁, t₂, rfl, Language.BoundedFormula.IsAtomic.equal t₁ t₂ |>.isQF⟩
  | rel R _ =>
      exact Empty.elim R

/-- Evaluation in the free commutative ring turns a ring term into its
universal integer polynomial. -/
noncomputable def polynomialOfTerm {alpha : Type} (t : Language.ring.Term alpha) :
    FreeCommRing alpha := by
  letI := FirstOrder.Ring.compatibleRingOfRing (FreeCommRing alpha)
  exact t.realize FreeCommRing.of

/-- The universal polynomial extracted from a term has the same value as the
term in every compatible commutative ring. -/
theorem realize_polynomialOfTerm
    {alpha R : Type} [CommRing R] [FirstOrder.Ring.CompatibleRing R]
    (v : alpha -> R) (t : Language.ring.Term alpha) :
    FreeCommRing.lift v (polynomialOfTerm t) = t.realize v := by
  induction t with
  | var x =>
      simp only [polynomialOfTerm, Language.Term.realize_var,
        FreeCommRing.lift_of]
  | func f ts ih =>
      cases f with
      | add =>
          change FreeCommRing.lift v
              (polynomialOfTerm (ts 0) + polynomialOfTerm (ts 1)) = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.add ts) =
              Term.realize v (ts 0) + Term.realize v (ts 1) by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.addFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_add _]
          simpa only [map_add] using
            congrArg₂ (.+.) (ih 0) (ih 1)
      | mul =>
          change FreeCommRing.lift v
              (polynomialOfTerm (ts 0) * polynomialOfTerm (ts 1)) = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.mul ts) =
              Term.realize v (ts 0) * Term.realize v (ts 1) by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.mulFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_mul _]
          simpa only [map_mul] using
            congrArg₂ (.*.) (ih 0) (ih 1)
      | neg =>
          change FreeCommRing.lift v (-polynomialOfTerm (ts 0)) = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.neg ts) =
              -Term.realize v (ts 0) by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.negFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_neg _]
          simpa only [map_neg] using
            congrArg Neg.neg (ih 0)
      | zero =>
          change FreeCommRing.lift v 0 = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.zero ts) = 0 by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.zeroFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_zero _]
          exact map_zero (FreeCommRing.lift v)
      | one =>
          change FreeCommRing.lift v 1 = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.one ts) = 1 by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.oneFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_one _]
          exact map_one (FreeCommRing.lift v)

/-- Atomic equality is equality of two universal integer polynomials in every
compatible commutative ring. This is the algebraic payload of the atomic
normalization branch; connecting all models of the selected complete theory
to this interface remains a separate theory/semantics obligation. -/
theorem atomicPolynomialNormalization
    {alpha : Type} {n : Nat}
    {phi : Language.ring.BoundedFormula alpha n} (hphi : phi.IsAtomic) :
    exists p q : FreeCommRing (alpha ⊕ Fin n),
      forall {R : Type} [CommRing R] [FirstOrder.Ring.CompatibleRing R]
          (v : alpha ⊕ Fin n -> R),
        phi.Realize (v ∘ Sum.inl) (v ∘ Sum.inr) <->
          FreeCommRing.lift v p = FreeCommRing.lift v q := by
  cases hphi with
  | equal t₁ t₂ =>
      refine ⟨polynomialOfTerm t₁, polynomialOfTerm t₂, ?_⟩
      intro R _ _ v
      change t₁.realize (Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr)) =
        t₂.realize (Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr)) <-> _
      have hv : Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr) = v := by
        funext x
        cases x <;> rfl
      rw [hv]
      rw [realize_polynomialOfTerm, realize_polynomialOfTerm]
  | rel R _ =>
      exact Empty.elim R

/-- The complete Boolean closure package used by the formula-recursion
branch. -/
theorem qfBooleanClosure
    {alpha : Type} {n : Nat}
    {phi psi : Language.ring.BoundedFormula alpha n}
    (hphi : phi.IsQF) (hpsi : psi.IsQF) :
    phi.not.IsQF ∧ (phi.imp psi).IsQF ∧
      (phi ⊓ psi).IsQF ∧ (phi ⊔ psi).IsQF := by
  exact ⟨hphi.not, hphi.imp hpsi, hphi.inf hpsi, hphi.sup hpsi⟩

/-- The exact remaining semantic core: eliminate one existentially bound
variable from any quantifier-free formula, uniformly with any other in-scope
bound variables and the unchanged free-variable type. -/
def OneVariableEliminationPackage : Prop :=
  forall {alpha : Type} {n : Nat}
      (phi : Language.ring.BoundedFormula alpha (n + 1)),
    phi.IsQF ->
      exists psi : Language.ring.BoundedFormula alpha n,
        psi.IsQF ∧ phi.ex ⇔[realClosedFieldTheory] psi

/-- Formula induction after the algebraic one-variable step is supplied.
Atomic and Boolean cases are discharged locally; the universal case is
rewritten as a negated existential and consumes the package exactly once. -/
theorem formulaElimination_of_oneVariable
    (oneVariable : OneVariableEliminationPackage) :
    forall {alpha : Type} {n : Nat}
        (phi : Language.ring.BoundedFormula alpha n),
      exists psi : Language.ring.BoundedFormula alpha n,
        psi.IsQF ∧ phi ⇔[realClosedFieldTheory] psi := by
  intro alpha n phi
  induction phi with
  | falsum =>
      exact qfEquivalent_of_isQF Language.BoundedFormula.isQF_bot
  | equal t₁ t₂ =>
      exact qfEquivalent_of_isQF
        (Language.BoundedFormula.IsAtomic.equal t₁ t₂).isQF
  | rel R _ =>
      exact Empty.elim R
  | imp phi psi ihphi ihpsi =>
      obtain ⟨phi', hphi', ephi⟩ := ihphi
      obtain ⟨psi', hpsi', epsi⟩ := ihpsi
      exact ⟨phi'.imp psi', hphi'.imp hpsi', ephi.imp epsi⟩
  | all phi ihphi =>
      obtain ⟨psi, hpsi, epsi⟩ := ihphi
      obtain ⟨theta, htheta, etheta⟩ := oneVariable psi.not hpsi.not
      exact ⟨theta.not, htheta.not,
        epsi.all |>.trans
          ((Language.BoundedFormula.all_iff_not_ex_not psi).trans etheta.not)⟩

/-- Checked final composition from the still-open algebraic package to the
unchanged canonical target.  This theorem exposes rather than hides the
remaining premise. -/
theorem tarskiQuantifierElimination_of_oneVariable
    (oneVariable : OneVariableEliminationPackage) :
    TarskiQuantifierEliminationTarget := by
  intro alpha phi
  exact formulaElimination_of_oneVariable oneVariable phi

#print axioms qfEquivalent_of_isQF
#print axioms atomicEqualityNormalization
#print axioms realize_polynomialOfTerm
#print axioms atomicPolynomialNormalization
#print axioms qfBooleanClosure
#print axioms formulaElimination_of_oneVariable
#print axioms tarskiQuantifierElimination_of_oneVariable

assert_no_sorry qfEquivalent_of_isQF
assert_no_sorry atomicEqualityNormalization
assert_no_sorry realize_polynomialOfTerm
assert_no_sorry atomicPolynomialNormalization
assert_no_sorry qfBooleanClosure
assert_no_sorry formulaElimination_of_oneVariable
assert_no_sorry tarskiQuantifierElimination_of_oneVariable

end Stage1.THM_M_0669
