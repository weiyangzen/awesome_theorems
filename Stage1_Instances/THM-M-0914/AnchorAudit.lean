import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-! The validator composes this probe with the statement source before elaboration. -/

/-!
# THM-M-0914 immutable anchor probes

This module checks an exact audit-local copy of the frozen finite pigeonhole target against the
pinned mathlib theorem. It is provisional anchor-audit evidence, not an accepted proof-phase or
theorem-completion declaration.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0914_AnchorAudit

/-- A literal audit-local copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  ∀ (n : Nat) (f : Fin (n + 1) → Fin n),
    ∃ x y, x ≠ y ∧ f x = f y

/-- Exact specialization of the pinned finite-type pigeonhole theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro n f
  exact Fintype.exists_ne_map_eq_of_card_lt f (by simp)

#check Fintype.exists_ne_map_eq_of_card_lt
#check Finset.exists_ne_map_eq_of_card_lt_of_maps_to
#check Fintype.not_injective_of_card_lt
#check Function.Embedding.isEmpty_of_card_lt

#print Fintype.exists_ne_map_eq_of_card_lt
#print Finset.exists_ne_map_eq_of_card_lt_of_maps_to

assert_no_sorry Fintype.exists_ne_map_eq_of_card_lt
assert_no_sorry Finset.exists_ne_map_eq_of_card_lt_of_maps_to
assert_no_sorry exactTarget_mathlib_candidate

#print sorries Fintype.exists_ne_map_eq_of_card_lt
#print sorries Finset.exists_ne_map_eq_of_card_lt_of_maps_to
#print sorries exactTarget_mathlib_candidate

#print axioms Fintype.exists_ne_map_eq_of_card_lt
#print axioms Finset.exists_ne_map_eq_of_card_lt_of_maps_to
#print axioms exactTarget_mathlib_candidate

open Lean Elab Command in
elab "#print_anchor_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Fintype.exists_ne_map_eq_of_card_lt,
    ``Finset.exists_ne_map_eq_of_card_lt_of_maps_to,
    ``Stage1Instances.THM_M_0914_AnchorAudit.exactTarget_mathlib_candidate
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
  logInfo m!"ANCHOR_CLOSURE declarations={closure.size} modules={modules.size}"
  logInfo m!"ANCHOR_CLOSURE axioms={uniqueAxioms.qsort Name.lt}"
  logInfo m!"ANCHOR_CLOSURE bodyless_nonaxioms={bodyless.qsort Name.lt}"
  logInfo m!"ANCHOR_CLOSURE unsafe={unsafeDecls.qsort Name.lt}"

#print_anchor_closure

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0914_AnchorAudit
