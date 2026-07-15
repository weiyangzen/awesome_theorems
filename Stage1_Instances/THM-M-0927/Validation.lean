import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0927 same-worker validation probe

This module reconstructs the exact frozen radical target directly from the
pinned function-level Binet theorem. It deliberately does not invoke the
proof-phase root declaration. The check is differential, but it shares the
checkout, toolchain, dependency cache, and terminal body with the proof and is
therefore not an independent-runner attestation.
-/

noncomputable section

namespace Stage1Instances.THM_M_0927.Validation

open Stage1Instances.THM_M_0927

/-- A fresh exact-root composition from the pinned terminal theorem and the
statement-phase representation transport. -/
theorem independentlyRecomposedBinetFormula : BinetFormulaTarget := by
  apply binetFormulaTarget_iff_characteristicRootTarget.mpr
  intro n
  exact congrFun Real.coe_fib_eq' n

#check independentlyRecomposedBinetFormula

assert_no_sorry Real.coe_fib_eq'
assert_no_sorry Stage1Instances.THM_M_0927.Proof.functionBinet_proof
assert_no_sorry Stage1Instances.THM_M_0927.Proof.binetFormula_proof
assert_no_sorry independentlyRecomposedBinetFormula

#print sorries Real.coe_fib_eq'
#print sorries Stage1Instances.THM_M_0927.Proof.functionBinet_proof
#print sorries Stage1Instances.THM_M_0927.Proof.binetFormula_proof
#print sorries independentlyRecomposedBinetFormula

#print axioms Real.coe_fib_eq'
#print axioms Stage1Instances.THM_M_0927.Proof.functionBinet_proof
#print axioms Stage1Instances.THM_M_0927.Proof.binetFormula_proof
#print axioms independentlyRecomposedBinetFormula

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0927.Proof.binetFormula_proof,
    ``Stage1Instances.THM_M_0927.Validation.independentlyRecomposedBinetFormula
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let rootAxioms <- roots.flatMapM collectAxioms
  let allowedAxioms := NameSet.ofArray rootAxioms
  let env <- getEnv
  let mut unexpectedBodyless : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if !allowedAxioms.contains name then
        unexpectedBodyless := unexpectedBodyless.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={allowedAxioms.toArray.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unexpected_bodyless={unexpectedBodyless.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1Instances.THM_M_0927.Validation
