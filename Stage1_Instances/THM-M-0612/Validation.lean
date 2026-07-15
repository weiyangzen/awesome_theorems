import DimensionTwo
import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0612 validation audit

This module rechecks the proof-phase dimension-two declarations and separately
reconstructs the conditional composition from the still-open universal
radius-squared obstruction to the exact canonical target. It does not supply
the higher-dimensional nonsqueezing argument and therefore does not prove the
canonical root.
-/

noncomputable section

namespace Stage1.THM_M_0612.Validation

universe u

open Stage1.THM_M_0612

/-- Separately written conditional composition against the frozen exact target. -/
theorem rootFromRadiusSquaredObstruction
    (geometry : RadiusSquaredObstruction.{u}) : StatementShape.{u} := by
  intro Q _ i r R hr hR f hf hmaps
  exact radius_le_of_sq_le hr hR (geometry Q i r R hr hR f hf hmaps)

assert_no_sorry symplectic_det_dimTwo
assert_no_sorry image_volume_eq_dimTwo
assert_no_sorry volume_ball_dimTwo
assert_no_sorry dimTwo_radiusSquaredObstruction
assert_no_sorry radius_le_of_sq_le
assert_no_sorry root_of_radiusSquaredObstruction
assert_no_sorry rootFromRadiusSquaredObstruction

#print sorries symplectic_det_dimTwo
  image_volume_eq_dimTwo
  volume_ball_dimTwo
  dimTwo_radiusSquaredObstruction
  radius_le_of_sq_le
  root_of_radiusSquaredObstruction
  rootFromRadiusSquaredObstruction

#print axioms symplectic_det_dimTwo
#print axioms image_volume_eq_dimTwo
#print axioms volume_ball_dimTwo
#print axioms dimTwo_radiusSquaredObstruction
#print axioms radius_le_of_sq_le
#print axioms root_of_radiusSquaredObstruction
#print axioms rootFromRadiusSquaredObstruction

open Lean Elab Command in
elab "#print_validation_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Stage1.THM_M_0612.symplectic_det_dimTwo,
    ``Stage1.THM_M_0612.image_volume_eq_dimTwo,
    ``Stage1.THM_M_0612.volume_ball_dimTwo,
    ``Stage1.THM_M_0612.dimTwo_radiusSquaredObstruction,
    ``Stage1.THM_M_0612.radius_le_of_sq_le,
    ``Stage1.THM_M_0612.root_of_radiusSquaredObstruction,
    ``Stage1.THM_M_0612.Validation.rootFromRadiusSquaredObstruction
  ]
  let closure <- NameSet.transitivelyUsedConstants (.ofArray roots)
  let axioms <- roots.flatMapM collectAxioms
  let uniqueAxioms := NameSet.ofArray axioms |>.toArray
  let env <- getEnv
  let mut unexpectedAxioms : Array Name := #[]
  let mut unsafeDecls : Array Name := #[]
  let mut modules : NameSet := {}
  for name in closure do
    let info <- getConstInfo name
    if info.isUnsafe then unsafeDecls := unsafeDecls.push name
    if let .axiomInfo _ := info then
      if name != ``propext && name != ``Classical.choice && name != ``Quot.sound then
        unexpectedAxioms := unexpectedAxioms.push name
    if let some moduleName := env.getModuleFor? name then
      modules := modules.insert moduleName
  logInfo m!"VALIDATION_CLOSURE roots={roots.size} declarations={closure.size} modules={modules.size}"
  logInfo m!"VALIDATION_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unexpected_axioms={unexpectedAxioms.qsort Name.lt}"
  logInfo m!"VALIDATION_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_validation_closure

end Stage1.THM_M_0612.Validation
