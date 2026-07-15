import Statement
import Mathlib.Computability.Reduce
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0709 validation probes

This module imports neither `Proof` nor `ObligationTree`. It independently
reconstructs the pinned halting leaf, the generic many-one pullback, and the
conditional composition into the exact frozen binary-PCP target. The required
halting-to-PCP reduction remains an explicit premise, so this file does not
close the root.

These are same-worker differential probes, not an independent-runner
attestation.
-/

namespace Stage1Instances.THM_M_0709.Validation

open Stage1Instances.THM_M_0709

/-- A separately spelled fixed-input source predicate. -/
def ValidationHaltingPredicate (input : Nat) (code : Nat.Partrec.Code) : Prop :=
  (Nat.Partrec.Code.eval code input).Dom

/-- Differential reconstruction of computable many-one pullback. -/
theorem manyOnePullback_validation
    {alpha beta : Type*} [Primcodable alpha] [Primcodable beta]
    {source : alpha -> Prop} {target : beta -> Prop}
    (hsource : ¬ ComputablePred source) (hred : source ≤₀ target) :
    ¬ ComputablePred target := by
  intro htarget
  exact hsource (ComputablePred.computable_of_manyOneReducible hred htarget)

/-- A direct wrapper over the pinned fixed-input halting theorem. -/
theorem haltingLeaf_validation (input : Nat) :
    ¬ ComputablePred (ValidationHaltingPredicate input) := by
  exact ComputablePred.halting_problem input

/-- Independent exact-type reconstruction of the terminal composition. The
reduction input is exactly the still-open root-critical package. -/
theorem conditionalRoot_validation
    (input : Nat)
    (hred : ValidationHaltingPredicate input ≤₀ HasSolution) :
    PostCorrespondenceUndecidable := by
  exact manyOnePullback_validation (haltingLeaf_validation input) hred

#check manyOnePullback_validation
#check haltingLeaf_validation
#check conditionalRoot_validation

assert_no_sorry ComputablePred.computable_of_manyOneReducible
assert_no_sorry ComputablePred.halting_problem
assert_no_sorry manyOnePullback_validation
assert_no_sorry haltingLeaf_validation
assert_no_sorry conditionalRoot_validation

#print sorries ComputablePred.computable_of_manyOneReducible
  ComputablePred.halting_problem manyOnePullback_validation
  haltingLeaf_validation conditionalRoot_validation

#print axioms ComputablePred.computable_of_manyOneReducible
#print axioms ComputablePred.halting_problem
#print axioms manyOnePullback_validation
#print axioms haltingLeaf_validation
#print axioms conditionalRoot_validation

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``ComputablePred.computable_of_manyOneReducible,
    ``ComputablePred.halting_problem,
    ``Stage1Instances.THM_M_0709.Validation.manyOnePullback_validation,
    ``Stage1Instances.THM_M_0709.Validation.haltingLeaf_validation,
    ``Stage1Instances.THM_M_0709.Validation.conditionalRoot_validation
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

end Stage1Instances.THM_M_0709.Validation
