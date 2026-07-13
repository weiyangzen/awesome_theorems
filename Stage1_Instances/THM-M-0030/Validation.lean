import Statement
import Mathlib.RingTheory.Filtration
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0030 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen Krull-intersection root directly from the pinned mathlib theorem. This is a separately
written same-worker check, not a distinct proof body or independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0030.Validation

open Stage1Instances.THM_M_0030

universe u

/-- A separately written exact-type specialization of the pinned finite-module theorem. -/
theorem differentialKrullIntersection : KrullIntersectionTarget.{u} := by
  intro R _ _ _ I hI
  convert Ideal.iInf_pow_smul_eq_bot_of_isLocalRing (M := R) I hI
  ext n
  rw [smul_eq_mul, <- Ideal.one_eq_top, mul_one]

assert_no_sorry Ideal.mem_iInf_smul_pow_eq_bot_iff
assert_no_sorry Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
assert_no_sorry Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
assert_no_sorry Ideal.iInf_pow_eq_bot_of_isLocalRing
assert_no_sorry differentialKrullIntersection

#print sorries Ideal.mem_iInf_smul_pow_eq_bot_iff
#print sorries Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print sorries Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#print sorries Ideal.iInf_pow_eq_bot_of_isLocalRing
#print sorries differentialKrullIntersection

#print axioms Ideal.mem_iInf_smul_pow_eq_bot_iff
#print axioms Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print axioms Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#print axioms Ideal.iInf_pow_eq_bot_of_isLocalRing
#print axioms differentialKrullIntersection

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Ideal.mem_iInf_smul_pow_eq_bot_iff,
    ``Ideal.iInf_pow_smul_eq_bot_of_le_jacobson,
    ``Ideal.iInf_pow_smul_eq_bot_of_isLocalRing,
    ``Ideal.iInf_pow_eq_bot_of_isLocalRing,
    ``Stage1Instances.THM_M_0030.Validation.differentialKrullIntersection
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

end Stage1Instances.THM_M_0030.Validation
