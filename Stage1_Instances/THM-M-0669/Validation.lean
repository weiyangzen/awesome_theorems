import Statement
import Mathlib.ModelTheory.Algebra.Ring.FreeCommRing
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0669 same-worker differential validation

This module imports neither `Proof` nor `ObligationTree`. It separately
reimplements the unconditional Boolean closure and the semantic reduction of
pure-ring atomic equalities to universal integer polynomials. It also checks
the final formula-recursion boundary from an explicit one-variable elimination
premise. That premise remains open, so this file does not prove the canonical
quantifier-elimination target.
-/

namespace Stage1.THM_M_0669.Validation

open FirstOrder FirstOrder.Language
open scoped FirstOrder
open Stage1.THM_M_0669

/-- Independent extraction of a ring term as a universal integer polynomial. -/
noncomputable def validationPolynomialOfTerm {alpha : Type}
    (t : Language.ring.Term alpha) : FreeCommRing alpha := by
  letI := FirstOrder.Ring.compatibleRingOfRing (FreeCommRing alpha)
  exact t.realize FreeCommRing.of

/-- The independently extracted polynomial realizes to the original term in
every compatible commutative ring. -/
theorem validation_realize_polynomialOfTerm
    {alpha R : Type} [CommRing R] [FirstOrder.Ring.CompatibleRing R]
    (v : alpha -> R) (t : Language.ring.Term alpha) :
    FreeCommRing.lift v (validationPolynomialOfTerm t) = t.realize v := by
  induction t with
  | var x =>
      simp only [validationPolynomialOfTerm, Language.Term.realize_var,
        FreeCommRing.lift_of]
  | func f ts ih =>
      cases f with
      | add =>
          change FreeCommRing.lift v
              (validationPolynomialOfTerm (ts 0) +
                validationPolynomialOfTerm (ts 1)) = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.add ts) =
              Term.realize v (ts 0) + Term.realize v (ts 1) by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.addFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_add _]
          simpa only [map_add] using congrArg₂ (.+.) (ih 0) (ih 1)
      | mul =>
          change FreeCommRing.lift v
              (validationPolynomialOfTerm (ts 0) *
                validationPolynomialOfTerm (ts 1)) = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.mul ts) =
              Term.realize v (ts 0) * Term.realize v (ts 1) by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.mulFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_mul _]
          simpa only [map_mul] using congrArg₂ (.*.) (ih 0) (ih 1)
      | neg =>
          change FreeCommRing.lift v
              (-validationPolynomialOfTerm (ts 0)) = _
          rw [show Term.realize v (Term.func FirstOrder.ringFunc.neg ts) =
              -Term.realize v (ts 0) by
            change FirstOrder.Language.Structure.funMap FirstOrder.Ring.negFunc
              (fun i => Term.realize v (ts i)) = _
            exact FirstOrder.Ring.CompatibleRing.funMap_neg _]
          simpa only [map_neg] using congrArg Neg.neg (ih 0)
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

/-- Independent semantic normalization of pure-ring atomic equalities. -/
theorem validationAtomicPolynomialNormalization
    {alpha : Type} {n : Nat}
    {phi : Language.ring.BoundedFormula alpha n} (hphi : phi.IsAtomic) :
    exists p q : FreeCommRing (alpha ⊕ Fin n),
      forall {R : Type} [CommRing R] [FirstOrder.Ring.CompatibleRing R]
          (v : alpha ⊕ Fin n -> R),
        phi.Realize (v ∘ Sum.inl) (v ∘ Sum.inr) <->
          FreeCommRing.lift v p = FreeCommRing.lift v q := by
  cases hphi with
  | equal t1 t2 =>
      refine ⟨validationPolynomialOfTerm t1,
        validationPolynomialOfTerm t2, ?_⟩
      intro R _ _ v
      change t1.realize (Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr)) =
        t2.realize (Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr)) <-> _
      have hv : Sum.elim (v ∘ Sum.inl) (v ∘ Sum.inr) = v := by
        funext x
        cases x <;> rfl
      rw [hv, validation_realize_polynomialOfTerm,
        validation_realize_polynomialOfTerm]
  | rel R _ =>
      exact Empty.elim R

/-- Independent Boolean `IsQF` closure, without importing the proof module. -/
theorem validationQfBooleanClosure
    {alpha : Type} {n : Nat}
    {phi psi : Language.ring.BoundedFormula alpha n}
    (hphi : phi.IsQF) (hpsi : psi.IsQF) :
    phi.not.IsQF ∧ (phi.imp psi).IsQF ∧
      (phi ⊓ psi).IsQF ∧ (phi ⊔ psi).IsQF := by
  exact ⟨hphi.not, hphi.imp hpsi, hphi.inf hpsi, hphi.sup hpsi⟩

/-- Local restatement of the still-open algebraic elimination interface. -/
def ValidationOneVariableElimination : Prop :=
  forall {alpha : Type} {n : Nat}
      (phi : Language.ring.BoundedFormula alpha (n + 1)),
    phi.IsQF ->
      exists psi : Language.ring.BoundedFormula alpha n,
        psi.IsQF ∧ phi.ex ⇔[realClosedFieldTheory] psi

/-- Independent formula recursion from the explicit open algebraic premise. -/
theorem validationFormulaElimination
    (oneVariable : ValidationOneVariableElimination) :
    forall {alpha : Type} {n : Nat}
        (phi : Language.ring.BoundedFormula alpha n),
      exists psi : Language.ring.BoundedFormula alpha n,
        psi.IsQF ∧ phi ⇔[realClosedFieldTheory] psi := by
  intro alpha n phi
  induction phi with
  | falsum =>
      exact ⟨⊥, Language.BoundedFormula.isQF_bot,
        Language.Theory.Iff.refl ⊥⟩
  | equal t1 t2 =>
      exact ⟨t1.bdEqual t2,
        (Language.BoundedFormula.IsAtomic.equal t1 t2).isQF,
        Language.Theory.Iff.refl (t1.bdEqual t2)⟩
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

/-- Conditional exact-root composition. The open one-variable package remains
an explicit premise and receives no root-closure credit. -/
theorem validationConditionalRoot
    (oneVariable : ValidationOneVariableElimination) :
    TarskiQuantifierEliminationTarget := by
  intro alpha phi
  exact validationFormulaElimination oneVariable phi

assert_no_sorry validation_realize_polynomialOfTerm
assert_no_sorry validationAtomicPolynomialNormalization
assert_no_sorry validationQfBooleanClosure
assert_no_sorry validationFormulaElimination
assert_no_sorry validationConditionalRoot

#print sorries validation_realize_polynomialOfTerm
#print sorries validationAtomicPolynomialNormalization
#print sorries validationQfBooleanClosure
#print sorries validationFormulaElimination
#print sorries validationConditionalRoot

#print axioms validation_realize_polynomialOfTerm
#print axioms validationAtomicPolynomialNormalization
#print axioms validationQfBooleanClosure
#print axioms validationFormulaElimination
#print axioms validationConditionalRoot

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1.THM_M_0669.Validation.validation_realize_polynomialOfTerm,
    ``Stage1.THM_M_0669.Validation.validationAtomicPolynomialNormalization,
    ``Stage1.THM_M_0669.Validation.validationQfBooleanClosure,
    ``Stage1.THM_M_0669.Validation.validationFormulaElimination,
    ``Stage1.THM_M_0669.Validation.validationConditionalRoot
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1.THM_M_0669.Validation
