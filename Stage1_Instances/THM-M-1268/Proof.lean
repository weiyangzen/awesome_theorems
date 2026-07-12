import Mathlib.Analysis.LocallyConvex.WeakSpace
import Mathlib.Topology.Semicontinuity.Basic
import Mathlib.Data.EReal.Basic

/-!
# THM-M-1268 proof execution

This module replays the frozen statement and obligation interfaces and supplies
placeholder-free proof bodies for the three open bridges.  The final theorem
inhabits the exact proposition frozen in `Statement.lean`.
-/

noncomputable section

namespace Stage1Instances.THM_M_1268.Proof

open Set

universe u

def IsExtendedRealConvex {E : Type u} [AddCommGroup E] [Module Real E]
    (f : E -> EReal) : Prop :=
  (forall x, f x != (⊥ : EReal)) /\
    forall (x y : E) (a b : Real), 0 <= a -> 0 <= b -> a + b = 1 ->
      f (a • x + b • y) <= (a : EReal) * f x + (b : EReal) * f y

def OnWeakSpace {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    (f : E -> EReal) : WeakSpace Real E -> EReal :=
  fun x => f ((toWeakSpace Real E).symm x)

def WeakLowerSemicontinuityTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    IsExtendedRealConvex f ->
      (LowerSemicontinuous (OnWeakSpace f) <-> LowerSemicontinuous f)

abbrev Sublevel {E : Type u} (f : E -> EReal) (r : EReal) : Set E :=
  f ⁻¹' Iic r

def ConvexSublevels {E : Type u} [AddCommGroup E] [Module Real E]
    (f : E -> EReal) : Prop :=
  forall r, Convex Real (Sublevel f r)

def NormClosedSublevels {E : Type u} [TopologicalSpace E]
    (f : E -> EReal) : Prop :=
  forall r, IsClosed (Sublevel f r)

def WeakClosedSublevels {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    (f : E -> EReal) : Prop :=
  forall r, IsClosed ((OnWeakSpace f) ⁻¹' Iic r)

/-- Jensen convexity makes every extended-real sublevel convex. -/
theorem convexSublevelBridge :
    forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
      IsExtendedRealConvex f -> ConvexSublevels f := by
  intro E _ _ f hf r x hx y hy a b ha hb hab
  refine (hf.2 x y a b ha hb hab).trans ?_
  calc
    (a : EReal) * f x + (b : EReal) * f y
        <= (a : EReal) * r + (b : EReal) * r := by
          exact add_le_add
            (mul_le_mul_of_nonneg_left hx (EReal.coe_nonneg.mpr ha))
            (mul_le_mul_of_nonneg_left hy (EReal.coe_nonneg.mpr hb))
    _ = r := by
      rw [← EReal.right_distrib_of_nonneg
        (EReal.coe_nonneg.mpr ha) (EReal.coe_nonneg.mpr hb),
        ← EReal.coe_add, hab, EReal.coe_one, one_mul]

/-- A norm-closed convex set is closed after transport to the weak space. -/
theorem weakClosed_of_convex_normClosed
    {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    {s : Set E} (hconvex : Convex Real s) (hclosed : IsClosed s) :
    IsClosed ((toWeakSpace Real E).symm ⁻¹' s) := by
  have himage : (toWeakSpace Real E) '' s =
      (toWeakSpace Real E).symm ⁻¹' s := by
    ext x
    constructor
    · rintro ⟨y, hy, rfl⟩
      simpa using hy
    · intro hx
      exact ⟨(toWeakSpace Real E).symm x, hx, by simp⟩
  rw [← himage, ← closure_eq_iff_isClosed]
  rw [← hconvex.toWeakSpace_closure Real, hclosed.closure_eq]

/-- Closed convex norm sublevels therefore become weakly closed sublevels. -/
theorem weakClosureTransportBridge :
    forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
      ConvexSublevels f -> NormClosedSublevels f -> WeakClosedSublevels f := by
  intro E _ _ f hconvex hclosed r
  exact weakClosed_of_convex_normClosed (hconvex r) (hclosed r)

/-- Weak lower semicontinuity implies norm lower semicontinuity by composing
with the continuous norm-to-weak identity map. -/
theorem weakToNormBridge :
    forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
      LowerSemicontinuous (OnWeakSpace f) -> LowerSemicontinuous f := by
  intro E _ _ f h
  simpa [OnWeakSpace] using
    h.comp (map_continuous (toWeakSpaceCLM Real E))

theorem normClosedSublevels_iff {E : Type u} [TopologicalSpace E] (f : E -> EReal) :
    NormClosedSublevels f <-> LowerSemicontinuous f := by
  exact lowerSemicontinuous_iff_isClosed_preimage.symm

theorem weakClosedSublevels_iff {E : Type u}
    [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal) :
    WeakClosedSublevels f <-> LowerSemicontinuous (OnWeakSpace f) := by
  exact lowerSemicontinuous_iff_isClosed_preimage.symm

/-- Placeholder-free proof of the exact frozen weak-lower-semicontinuity target. -/
theorem weakLowerSemicontinuity : WeakLowerSemicontinuityTarget.{u} := by
  intro E _ _ f hf
  constructor
  · exact weakToNormBridge E f
  · intro hlsc
    apply (weakClosedSublevels_iff f).mp
    exact weakClosureTransportBridge E f (convexSublevelBridge E f hf)
      ((normClosedSublevels_iff f).mpr hlsc)

#print axioms convexSublevelBridge
#print axioms weakClosed_of_convex_normClosed
#print axioms weakClosureTransportBridge
#print axioms weakToNormBridge
#print axioms weakLowerSemicontinuity

end Stage1Instances.THM_M_1268.Proof
