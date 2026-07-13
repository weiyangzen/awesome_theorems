import Mathlib.Combinatorics.Additive.AP.Three.Behrend
import Mathlib.Analysis.SpecialFunctions.Log.Base
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0958 immutable anchor probes

This module checks the pinned Behrend lower-bound family and guards its strict
quantitative mismatch with the frozen Elkin target. It is candidate evidence
for the anchor-audit phase only, not a proof of the Elkin construction.
-/

noncomputable section

open Finset

namespace Stage1Instances.THM_M_0958_AnchorAudit

/-- Audit-local literal copy of the statement phase's quantitative scale. -/
def exactElkinScale (n : Nat) : Real :=
  ((n : Real) /
      (2 : Real) ^ (2 * Real.sqrt 2 * Real.sqrt (Real.logb 2 (n : Real)))) *
    (Real.logb 2 (n : Real)) ^ (1 / 4 : Real)

/-- Audit-local literal copy of the frozen canonical proposition. -/
def ExactElkinTarget : Prop :=
  exists c : Real, 0 < c /\ exists N : Nat, 0 < N /\ forall n : Nat, N <= n ->
    c * exactElkinScale n <= (addRothNumber (Ico 1 (n + 1)) : Real)

/-- The proposition actually supplied by pinned mathlib's Behrend theorem. -/
def PinnedBehrendTarget : Prop :=
  forall N : Nat,
    (N : Real) * Real.exp (-4 * Real.sqrt (Real.log N)) <=
      (rothNumberNat N : Real)

/-- Audit-only wrapper around the genuine pinned Behrend proof body. -/
theorem pinnedBehrendCandidate : PinnedBehrendTarget := by
  intro N
  exact Behrend.roth_lower_bound

/- The checked Behrend proposition is not definitionally the Elkin target. -/
#check_failure (rfl : ExactElkinTarget = PinnedBehrendTarget)

#check Behrend.card_sphere_le_rothNumberNat
#check Behrend.bound_aux
#check Behrend.roth_lower_bound_explicit
#check Behrend.roth_lower_bound

set_option pp.proofs false in
#print Behrend.roth_lower_bound_explicit
set_option pp.proofs false in
#print Behrend.roth_lower_bound

assert_no_sorry Behrend.roth_lower_bound_explicit
assert_no_sorry Behrend.roth_lower_bound
assert_no_sorry pinnedBehrendCandidate

#print sorries Behrend.roth_lower_bound_explicit
#print sorries Behrend.roth_lower_bound
#print sorries pinnedBehrendCandidate

#print axioms Behrend.roth_lower_bound_explicit
#print axioms Behrend.roth_lower_bound
#print axioms pinnedBehrendCandidate

open Lean Elab Command in
elab "#print_anchor_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Behrend.roth_lower_bound_explicit,
    ``Behrend.roth_lower_bound,
    ``Stage1Instances.THM_M_0958_AnchorAudit.pinnedBehrendCandidate
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

set_option pp.explicit true in
set_option pp.universes true in
#print ExactElkinTarget

end Stage1Instances.THM_M_0958_AnchorAudit
