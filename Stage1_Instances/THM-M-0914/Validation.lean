import Statement
import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0914 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen root through the noninjectivity interface rather than the proof phase's finite-set collision
wrapper. This is useful differential evidence, but it is not a distinct-runner attestation and it
does not create a second terminal proof body.
-/

namespace Stage1Instances.THM_M_0914.Validation

open Stage1Instances.THM_M_0914

/-- A separately written exact-root reconstruction through noninjectivity. -/
theorem pigeonholeTarget_differential : PigeonholeTarget := by
  intro n f
  have hCard : Fintype.card (Fin n) < Fintype.card (Fin (n + 1)) := by
    simp
  have hNotInjective : Not (Function.Injective f) :=
    Fintype.not_injective_of_card_lt f hCard
  obtain ⟨x, y, hMap, hNe⟩ := Function.not_injective_iff.mp hNotInjective
  exact ⟨x, y, hNe, hMap⟩

assert_no_sorry Fintype.not_injective_of_card_lt
assert_no_sorry Function.not_injective_iff
assert_no_sorry pigeonholeTarget_differential

#print sorries Fintype.not_injective_of_card_lt
#print sorries Function.not_injective_iff
#print sorries pigeonholeTarget_differential

#print axioms Fintype.not_injective_of_card_lt
#print axioms Function.not_injective_iff
#print axioms pigeonholeTarget_differential

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Fintype.not_injective_of_card_lt,
    ``Function.not_injective_iff,
    ``Stage1Instances.THM_M_0914.Validation.pigeonholeTarget_differential
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

end Stage1Instances.THM_M_0914.Validation
