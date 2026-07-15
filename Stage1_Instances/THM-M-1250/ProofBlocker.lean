import Statement

/-!
# THM-M-1250 proof-phase blocker witnesses

The frozen statement's unscoped `⊤` elaborates at a strictly stronger
`ContDiff` order than the `SchwartzMap.smooth'` field. These declarations
kernel-check the exact mismatch without asserting either open package.
-/

noncomputable section

open scoped ContDiff

namespace Stage1Instances.THM_M_1250

/-- Local spelling of the frozen reverse interface. -/
def FrozenReversePackage : Prop :=
  forall (n : Nat) (f : EuclideanDomain n -> Complex),
    IsSchwartzFunction f ->
      exists phi : SchwartzMap (EuclideanDomain n) Complex,
        (phi : EuclideanDomain n -> Complex) = f

/-- The two smoothness propositions that the frozen forward route would have
to identify. -/
def FrozenSmoothnessMismatch (n : Nat)
    (phi : SchwartzMap (EuclideanDomain n) Complex) : Prop :=
  ContDiff Real (⊤ : WithTop ENat) (phi : EuclideanDomain n -> Complex) ↔
    ContDiff Real (↑(⊤ : ENat) : WithTop ENat) phi.toFun

/-- The frozen order is definitionally mathlib's analytic order. -/
theorem frozen_top_is_analytic_order {n : Nat}
    (f : EuclideanDomain n -> Complex) :
    ContDiff Real (⊤ : WithTop ENat) f = ContDiff Real ω f := rfl

/-- The structure field uses mathlib's infinitely differentiable order. -/
theorem coerced_enat_top_is_smooth_order {n : Nat}
    (f : EuclideanDomain n -> Complex) :
    ContDiff Real (↑(⊤ : ENat) : WithTop ENat) f = ContDiff Real ∞ f := rfl

/-- The constructor's `C^infinity` field can be weakened from the frozen
stronger condition, so the reverse package remains constructible. -/
theorem reversePackage_from_frozen_conditions : FrozenReversePackage := by
  intro n f hf
  rcases hf with ⟨hsmooth, hdecay⟩
  refine ⟨⟨f, ?_, hdecay⟩, rfl⟩
  exact hsmooth.of_le le_top

set_option pp.explicit true in
#check FrozenSmoothnessMismatch
#check frozen_top_is_analytic_order
#check coerced_enat_top_is_smooth_order
set_option pp.explicit true in
#check @SchwartzMap.smooth'
#check reversePackage_from_frozen_conditions
#print axioms frozen_top_is_analytic_order
#print axioms coerced_enat_top_is_smooth_order
#print axioms reversePackage_from_frozen_conditions

end Stage1Instances.THM_M_1250
