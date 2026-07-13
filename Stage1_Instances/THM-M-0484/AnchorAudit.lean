import Mathlib.NumberTheory.LucasLehmer
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries
import ImportGraph.Imports.RequiredModules

/-!
# THM-M-0484 immutable mathlib anchor

This module independently restates the frozen target and checks the exact composition of the two
correctness directions in the manifest-pinned mathlib. It is evidence for the anchor-audit phase,
not the canonical proof-phase declaration or an accepted theorem-completion receipt.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0484.AnchorAudit

/-- Literal audit copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  forall p : Nat, 3 <= p ->
    (LucasLehmer.LucasLehmerTest p <-> Nat.Prime (mersenne p))

/-- Exact audit wrapper over the two pinned mathlib terminal directions. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro p hp
  constructor
  · exact lucas_lehmer_sufficiency p (by omega)
  · exact lucas_lehmer_necessity p hp

#check lucas_lehmer_sufficiency
#check lucas_lehmer_necessity
#check LucasLehmer.residue_eq_zero_iff_sMod_eq_zero

assert_no_sorry lucas_lehmer_sufficiency
assert_no_sorry lucas_lehmer_necessity
assert_no_sorry exactTarget_mathlib_candidate
#print sorries lucas_lehmer_sufficiency lucas_lehmer_necessity exactTarget_mathlib_candidate
#print axioms lucas_lehmer_sufficiency
#print axioms lucas_lehmer_necessity
#print axioms exactTarget_mathlib_candidate
#print exactTarget_mathlib_candidate

open Lean Elab Command in
elab "#print_anchor_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``lucas_lehmer_sufficiency,
    ``lucas_lehmer_necessity,
    ``Stage1Instances.THM_M_0484.AnchorAudit.exactTarget_mathlib_candidate
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

end Stage1Instances.THM_M_0484.AnchorAudit
