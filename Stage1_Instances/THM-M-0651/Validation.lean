import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0651 same-worker differential validation

This module deliberately imports neither `ProofLemmas` nor `ObligationTree`.
It independently reconstructs the checked omission transport, the fair
avoidance schedule, and the nonprincipality density step against the frozen
statement. It does not construct a Henkin model or prove the omitting-types
root.
-/

namespace Stage1Instances.THM_M_0651.Validation

open Set FirstOrder FirstOrder.Language
open Stage1Instances.THM_M_0651

universe u v w

/-- A no-import reconstruction of the checked omission transport. -/
theorem differentialOmitsIffNoRealizingTuple
    {L : Language.{u, v}} (M : Type*) [L.Structure M]
    {alpha : Type w} (p : Set (L.Formula alpha)) :
    Omits M p ↔ ¬∃ a : alpha -> M, ∀ phi ∈ p, phi.Realize a := by
  simp only [Omits, not_exists]
  apply forall_congr'
  intro a
  push Not
  rfl

/-- The syntax and tuple requirements used by a simultaneous construction
form a nonempty countable type and therefore admit a fair schedule. -/
theorem differentialExistsSurjectiveAvoidanceSchedule
    (L : Language.{u, v}) (arity : Nat -> Nat)
    [forall n, Countable (L.Functions n)]
    [forall n, Countable (L.Relations n)] :
    exists schedule : Nat ->
        ((Sigma fun n : Nat => L.Formula (Fin n)) ⊕
          (Sigma fun i : Nat => Fin (arity i) -> Nat)),
      Function.Surjective schedule := by
  letI : Countable L.Symbols := by
    unfold Language.Symbols
    infer_instance
  letI : Countable
      ((Sigma fun n : Nat => L.Formula (Fin n)) ⊕
        (Sigma fun i : Nat => Fin (arity i) -> Nat)) := by
    infer_instance
  exact exists_surjective_nat _

/-- Direct reconstruction of the dense avoidance consequence of the frozen
nonprincipality predicate. -/
theorem differentialExistsConsistentAvoidanceExtension
    {L : Language.{u, v}} {T : L.Theory} {alpha : Type w}
    {p : Set (L.Formula alpha)}
    (hnonprincipal : IsNonprincipal T p)
    {phi : L.Formula alpha}
    (hphi : ((L.lhomWithConstants alpha).onTheory T ∪
      {Formula.equivSentence phi}).IsSatisfiable) :
    ∃ psi ∈ p,
      ((L.lhomWithConstants alpha).onTheory T ∪
        {(Formula.equivSentence (phi.imp psi)).not}).IsSatisfiable := by
  classical
  have hnotall : ¬ ∀ psi ∈ p, T ⊨ᵇ phi.imp psi := by
    intro hall
    exact hnonprincipal phi ⟨hphi, hall⟩
  push Not at hnotall
  obtain ⟨psi, hpsi, hnotmodels⟩ := hnotall
  refine ⟨psi, hpsi, ?_⟩
  rw [Theory.models_formula_iff_onTheory_models_equivSentence,
    Theory.models_iff_not_satisfiable] at hnotmodels
  exact Classical.byContradiction hnotmodels

assert_no_sorry differentialOmitsIffNoRealizingTuple
assert_no_sorry differentialExistsSurjectiveAvoidanceSchedule
assert_no_sorry differentialExistsConsistentAvoidanceExtension

#print sorries differentialOmitsIffNoRealizingTuple
#print sorries differentialExistsSurjectiveAvoidanceSchedule
#print sorries differentialExistsConsistentAvoidanceExtension

#print axioms differentialOmitsIffNoRealizingTuple
#print axioms differentialExistsSurjectiveAvoidanceSchedule
#print axioms differentialExistsConsistentAvoidanceExtension

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0651.Validation.differentialOmitsIffNoRealizingTuple,
    ``Stage1Instances.THM_M_0651.Validation.differentialExistsSurjectiveAvoidanceSchedule,
    ``Stage1Instances.THM_M_0651.Validation.differentialExistsConsistentAvoidanceExtension
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
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0651.Validation
