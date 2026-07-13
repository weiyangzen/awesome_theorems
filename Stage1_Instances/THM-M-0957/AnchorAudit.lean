import Mathlib.Combinatorics.Additive.AP.Three.Behrend
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0957 immutable anchor probes

This module checks the pinned mathlib Behrend declarations against an audit-local copy of the
frozen historical target. The mathlib bounds and construction lemmas are useful proof anchors, but
their fixed constant-four conclusion is not the historical epsilon-dependent conclusion. Nothing
in this file is a proof of the canonical target.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0957_AnchorAudit

/-- Literal audit-local copy of the statement phase's frozen canonical target. -/
def ExactTarget : Prop :=
  forall epsilon : Real, 0 < epsilon ->
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat (N + 1) : Real)

/-- Exact proposition supplied by mathlib's large-`N` terminal declaration. -/
def MathlibExplicitTarget : Prop :=
  forall N : Nat, 4096 <= N ->
    (N : Real) * Real.exp (-4 * Real.sqrt (Real.log (N : Real))) <
      (rothNumberNat N : Real)

/-- Exact proposition supplied by mathlib's all-`N` terminal declaration. -/
def MathlibAllNTarget : Prop :=
  forall N : Nat,
    (N : Real) * Real.exp (-4 * Real.sqrt (Real.log (N : Real))) <=
      (rothNumberNat N : Real)

/-- Checked adapter to the pinned explicit candidate's own conclusion, not to `ExactTarget`. -/
theorem mathlibExplicitCandidate : MathlibExplicitTarget := by
  intro N hN
  exact Behrend.roth_lower_bound_explicit hN

/-- Checked adapter to the pinned all-`N` candidate's own conclusion, not to `ExactTarget`. -/
theorem mathlibAllNCandidate : MathlibAllNTarget := by
  intro N
  exact Behrend.roth_lower_bound

/-- At the admissible value epsilon = 1, the historical exponent constant is strictly below the
fixed constant four used by the terminal mathlib bounds. Thus the fixed-constant conclusion is not
the same quantitative statement and cannot be treated as an exact monotonicity wrapper. -/
theorem historicalConstantAtOne_lt_mathlibConstant :
    2 * Real.sqrt (2 * Real.log 2) + 1 < (4 : Real) := by
  have hsqrt : Real.sqrt (2 * Real.log 2) < (3 / 2 : Real) := by
    rw [Real.sqrt_lt' (by norm_num : (0 : Real) < 3 / 2)]
    nlinarith [Real.log_two_lt_d9]
  nlinarith

/-- The explicit mathlib theorem does give a restricted historical-shaped bound when the requested
constant is at least four. This records the exact reusable scope without broadening the root. -/
theorem mathlibCandidate_restricted
    (epsilon : Real) (hconstant : 4 <= 2 * Real.sqrt (2 * Real.log 2) + epsilon) :
    exists N0 : Nat, forall N : Nat, N0 <= N ->
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <
        (rothNumberNat (N + 1) : Real) := by
  refine ⟨4096, ?_⟩
  intro N hN
  have hNreal : (1 : Real) < (N : Real) := by
    exact_mod_cast (show 1 < N from lt_of_lt_of_le (by norm_num) hN)
  have hlog : 0 < Real.log (N : Real) := Real.log_pos hNreal
  have hsqrt : 0 < Real.sqrt (Real.log (N : Real)) := Real.sqrt_pos.2 hlog
  have hpower :
      (N : Real) ^
          (1 - (2 * Real.sqrt (2 * Real.log 2) + epsilon) /
            Real.sqrt (Real.log (N : Real))) <=
        (N : Real) * Real.exp (-4 * Real.sqrt (Real.log (N : Real))) := by
    have hNpos : 0 < (N : Real) := hNreal.trans' Real.zero_lt_one
    rw [Real.rpow_def_of_pos hNpos, ← Real.exp_log hNpos, ← Real.exp_add,
      Real.exp_le_exp]
    simp only [Real.log_exp]
    have hs_sq : Real.sqrt (Real.log (N : Real)) ^ 2 = Real.log (N : Real) :=
      Real.sq_sqrt hlog.le
    field_simp
    nlinarith
  exact hpower.trans_lt <|
    (Behrend.roth_lower_bound_explicit hN).trans_le <| by
      exact_mod_cast rothNumberNat.mono (Nat.le_succ N)

#check Behrend.threeAPFree_sphere
#check Behrend.threeAPFree_image_sphere
#check Behrend.card_sphere_le_rothNumberNat
#check Behrend.bound_aux
#check Behrend.roth_lower_bound_explicit
#check Behrend.roth_lower_bound

#check_failure (rfl : ExactTarget = MathlibExplicitTarget)
#check_failure (rfl : ExactTarget = MathlibAllNTarget)

assert_no_sorry Behrend.threeAPFree_image_sphere
assert_no_sorry Behrend.card_sphere_le_rothNumberNat
assert_no_sorry Behrend.bound_aux
assert_no_sorry Behrend.roth_lower_bound_explicit
assert_no_sorry Behrend.roth_lower_bound
assert_no_sorry mathlibExplicitCandidate
assert_no_sorry mathlibAllNCandidate
assert_no_sorry historicalConstantAtOne_lt_mathlibConstant
assert_no_sorry mathlibCandidate_restricted

#print sorries Behrend.threeAPFree_image_sphere
#print sorries Behrend.card_sphere_le_rothNumberNat
#print sorries Behrend.bound_aux
#print sorries Behrend.roth_lower_bound_explicit
#print sorries Behrend.roth_lower_bound
#print sorries mathlibExplicitCandidate
#print sorries mathlibAllNCandidate
#print sorries historicalConstantAtOne_lt_mathlibConstant
#print sorries mathlibCandidate_restricted

#print axioms Behrend.threeAPFree_image_sphere
#print axioms Behrend.card_sphere_le_rothNumberNat
#print axioms Behrend.bound_aux
#print axioms Behrend.roth_lower_bound_explicit
#print axioms Behrend.roth_lower_bound
#print axioms mathlibExplicitCandidate
#print axioms mathlibAllNCandidate
#print axioms historicalConstantAtOne_lt_mathlibConstant
#print axioms mathlibCandidate_restricted

open Lean Elab Command in
elab "#print_anchor_closure" : command => liftTermElabM do
  let roots : Array Name := #[
    ``Behrend.threeAPFree_image_sphere,
    ``Behrend.card_sphere_le_rothNumberNat,
    ``Behrend.bound_aux,
    ``Behrend.roth_lower_bound_explicit,
    ``Behrend.roth_lower_bound,
    ``Stage1Instances.THM_M_0957_AnchorAudit.mathlibExplicitCandidate,
    ``Stage1Instances.THM_M_0957_AnchorAudit.mathlibAllNCandidate,
    ``Stage1Instances.THM_M_0957_AnchorAudit.historicalConstantAtOne_lt_mathlibConstant,
    ``Stage1Instances.THM_M_0957_AnchorAudit.mathlibCandidate_restricted
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

end Stage1Instances.THM_M_0957_AnchorAudit
