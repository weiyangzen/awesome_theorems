import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0317 same-worker differential validation

This module imports neither `Proof` nor `ObligationTree`. It independently
spells the compactness-limit interface and reconstructs its proof from the
hash-bound statement imports. The finite-dimensional approximation package
and the exact Tychonoff root remain open.
-/

universe u

namespace AwesomeTheorems.THM_M_0317.Validation

/-- A separately spelled copy of the frozen small-displacement predicate. -/
def ValidationHasArbitrarilySmallDisplacement {E : Type u} [AddCommGroup E]
    [TopologicalSpace E] (K : Set E) (f : E -> E) : Prop :=
  forall V : Set E, V ∈ nhds (0 : E) -> ∃ x, x ∈ K ∧ f x - x ∈ V

/-- A separately spelled copy of the frozen compactness-limit package. -/
def ValidationCompactnessLimitPackage : Prop :=
  forall {E : Type u} [AddCommGroup E] [Module Real E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E),
      K.Nonempty -> IsCompact K -> Convex Real K -> Continuous f ->
        Set.MapsTo f K K -> ValidationHasArbitrarilySmallDisplacement K f ->
          ∃ x, x ∈ K ∧ Function.IsFixedPt f x

/-- Differential exact-type reconstruction of the compactness-limit branch. -/
theorem compactnessLimitPackage_validation :
    ValidationCompactnessLimitPackage.{u} := by
  intro E _ _ _ _ _ _ _ K f _ hcompact _ hf _ happrox
  have hclosure : (0 : E) ∈ closure ((fun x => f x - x) '' K) := by
    rw [mem_closure_iff_nhds]
    intro V hV
    obtain ⟨x, hxK, hxV⟩ := happrox V hV
    exact ⟨f x - x, hxV, x, hxK, rfl⟩
  have hclosed : IsClosed ((fun x => f x - x) '' K) :=
    (hcompact.image (hf.sub continuous_id)).isClosed
  have hzero : (0 : E) ∈ (fun x => f x - x) '' K := hclosed.closure_eq ▸ hclosure
  obtain ⟨x, hxK, hxzero⟩ := hzero
  exact ⟨x, hxK, sub_eq_zero.mp hxzero⟩

/-- A separately written conditional route from the still-open approximation
interface to the exact frozen Tychonoff target. -/
theorem conditionalExactRoot_validation
    (approximation : forall {E : Type u} [AddCommGroup E] [Module Real E]
      [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
      [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E),
        K.Nonempty -> IsCompact K -> Convex Real K -> Continuous f ->
          Set.MapsTo f K K -> ValidationHasArbitrarilySmallDisplacement K f) :
    forall {E : Type u} [AddCommGroup E] [Module Real E]
      [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
      [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E),
        TychonoffFixedPointTarget K f := by
  intro E _ _ _ _ _ _ _ K f hK hc hconv hf hmaps
  exact compactnessLimitPackage_validation K f hK hc hconv hf hmaps
    (approximation K f hK hc hconv hf hmaps)

assert_no_sorry AwesomeTheorems.THM_M_0317.ambient_subtype_fixed_point_iff
assert_no_sorry AwesomeTheorems.THM_M_0317.empty_boundary_rejects_removed_nonempty
assert_no_sorry AwesomeTheorems.THM_M_0317.ambient_domain_does_not_imply_member_domain
assert_no_sorry AwesomeTheorems.THM_M_0317.fixed_point_cannot_precede_map_binder
assert_no_sorry AwesomeTheorems.THM_M_0317.interval_rejects_removed_mapsTo
assert_no_sorry compactnessLimitPackage_validation
assert_no_sorry conditionalExactRoot_validation
#print sorries AwesomeTheorems.THM_M_0317.ambient_subtype_fixed_point_iff
#print sorries AwesomeTheorems.THM_M_0317.empty_boundary_rejects_removed_nonempty
#print sorries AwesomeTheorems.THM_M_0317.ambient_domain_does_not_imply_member_domain
#print sorries AwesomeTheorems.THM_M_0317.fixed_point_cannot_precede_map_binder
#print sorries AwesomeTheorems.THM_M_0317.interval_rejects_removed_mapsTo
#print sorries compactnessLimitPackage_validation
#print sorries conditionalExactRoot_validation
#print axioms AwesomeTheorems.THM_M_0317.ambient_subtype_fixed_point_iff
#print axioms AwesomeTheorems.THM_M_0317.empty_boundary_rejects_removed_nonempty
#print axioms AwesomeTheorems.THM_M_0317.ambient_domain_does_not_imply_member_domain
#print axioms AwesomeTheorems.THM_M_0317.fixed_point_cannot_precede_map_binder
#print axioms AwesomeTheorems.THM_M_0317.interval_rejects_removed_mapsTo
#print axioms compactnessLimitPackage_validation
#print axioms conditionalExactRoot_validation

end AwesomeTheorems.THM_M_0317.Validation
