import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0319 same-worker validation probe

This module recomposes the exact frozen root from the three substantive local
proof declarations rather than invoking `brouwerFixedPoint`. It is a
differential composition check inside the same worker, checkout, toolchain,
and dependency cache, not an independent proof or second-runner attestation.
-/

namespace Stage1Instances.THM_M_0319.Validation

/-- Recompose the canonical target without invoking the terminal local root. -/
theorem recomposedBrouwerFixedPoint : BrouwerFixedPointTarget := by
  intro n K f hne hcompact hconv hcont hmap
  exact exactFixedPoint _ K f hcompact hcont
    (hasApproximateFixedPoints _ K f hne hcompact hconv hcont hmap)

assert_no_sorry IndexedLOrder.Scarf
assert_no_sorry IndexedLOrder.GiComponentStructure_holds
assert_no_sorry Brouwer
assert_no_sorry Stage1Instances.THM_M_0319.exists_simplex_approximation
assert_no_sorry Stage1Instances.THM_M_0319.hasApproximateFixedPoints
assert_no_sorry Stage1Instances.THM_M_0319.exactFixedPoint
assert_no_sorry Stage1Instances.THM_M_0319.brouwerFixedPoint
assert_no_sorry recomposedBrouwerFixedPoint

#print sorries Stage1Instances.THM_M_0319.brouwerFixedPoint
#print sorries recomposedBrouwerFixedPoint
#print axioms Stage1Instances.THM_M_0319.brouwerFixedPoint
#print axioms recomposedBrouwerFixedPoint

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1Instances.THM_M_0319.brouwerFixedPoint,
    ``Stage1Instances.THM_M_0319.Validation.recomposedBrouwerFixedPoint
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

end Stage1Instances.THM_M_0319.Validation
