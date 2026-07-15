import Statement
import Mathlib.Computability.Reduce
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0711 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It
separately reconstructs the quotient boundary, generic many-one transfer,
pinned halting leaf, and conditional final adapter checked by the proof phase.
The missing halting-to-finite-presentation reduction remains an explicit
premise, so this module does not prove `NovikovBooneTarget` unconditionally.
-/

namespace Stage1.THM_M_0711.Validation

/-- A separately defined copy of the identity predicate for a fixed finite
presentation. -/
def DifferentialIdentityPred (n : Nat)
    (rels : Finset (FreeGroup (Fin n)))
    (word : List (Fin n × Bool)) : Prop :=
  PresentedGroup.mk (rels : Set (FreeGroup (Fin n))) (evalWord word) = 1

/-- No-import rederivation of the quotient normalization boundary. -/
theorem differentialIdentityPredIffNormalClosure (n : Nat)
    (rels : Finset (FreeGroup (Fin n))) (word : List (Fin n × Bool)) :
    DifferentialIdentityPred n rels word ↔
      evalWord word ∈ Subgroup.normalClosure (rels : Set (FreeGroup (Fin n))) := by
  exact PresentedGroup.mk_eq_one_iff

/-- No-import rederivation of noncomputability transfer along a many-one
reduction. -/
theorem differentialNotComputablePredOfManyOne
    {alpha beta : Type*} [Primcodable alpha] [Primcodable beta]
    {source : alpha → Prop} {target : beta → Prop}
    (hsource : ¬ComputablePred source) (hred : source ≤₀ target) :
    ¬ComputablePred target := by
  intro htarget
  exact hsource (ComputablePred.computable_of_manyOneReducible hred htarget)

/-- Direct use of the pinned fixed-input halting theorem. -/
theorem differentialHaltingPredicateNotComputable (input : Nat) :
    ¬ComputablePred fun code : Nat.Partrec.Code =>
      (Nat.Partrec.Code.eval code input).Dom := by
  exact ComputablePred.halting_problem input

/-- Independently checked final adapter. The central Novikov-Boone reduction
is deliberately visible as a premise and receives no root-closure credit. -/
theorem differentialConditionalTarget
    (n : Nat) (rels : Finset (FreeGroup (Fin n))) (input : Nat)
    (hred : (fun code : Nat.Partrec.Code =>
      (Nat.Partrec.Code.eval code input).Dom) ≤₀
        DifferentialIdentityPred n rels) :
    NovikovBooneTarget := by
  refine ⟨n, rels, ?_⟩
  exact differentialNotComputablePredOfManyOne
    (differentialHaltingPredicateNotComputable input) hred

assert_no_sorry differentialIdentityPredIffNormalClosure
assert_no_sorry differentialNotComputablePredOfManyOne
assert_no_sorry differentialHaltingPredicateNotComputable
assert_no_sorry differentialConditionalTarget

#print sorries differentialIdentityPredIffNormalClosure
#print sorries differentialNotComputablePredOfManyOne
#print sorries differentialHaltingPredicateNotComputable
#print sorries differentialConditionalTarget

#print axioms differentialIdentityPredIffNormalClosure
#print axioms differentialNotComputablePredOfManyOne
#print axioms differentialHaltingPredicateNotComputable
#print axioms differentialConditionalTarget

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1.THM_M_0711.Validation.differentialIdentityPredIffNormalClosure,
    ``Stage1.THM_M_0711.Validation.differentialNotComputablePredOfManyOne,
    ``Stage1.THM_M_0711.Validation.differentialHaltingPredicateNotComputable,
    ``Stage1.THM_M_0711.Validation.differentialConditionalTarget
  ]
  let closure ← NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms ← roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env ← getEnv
  let mut bodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info ← getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !axioms.contains name then bodyless := bodyless.push name
    if let some moduleName := env.getModuleFor? name then modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1.THM_M_0711.Validation
