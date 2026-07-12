import Mathlib.Analysis.LocallyConvex.WeakSpace
import Mathlib.Topology.Semicontinuity.Basic
import Mathlib.Data.EReal.Basic

/-!
# THM-M-1268 obligation interfaces

These declarations type-check the frozen proof architecture.  The composition
results are conditional: they do not provide any open mathematical bridge or
prove the root theorem.
-/

namespace Stage1Instances.THM_M_1268

universe u

-- Exact local replay of the frozen statement interfaces, needed because this
-- standalone validation file is intentionally outside the Lake source tree.
def IsExtendedRealConvex {E : Type u} [AddCommGroup E] [Module Real E]
    (f : E -> EReal) : Prop :=
  (forall x, f x != (⊥ : EReal)) /\
    forall (x y : E) (a b : Real), 0 <= a -> 0 <= b -> a + b = 1 ->
      f (a • x + b • y) <= (a : EReal) * f x + (b : EReal) * f y

noncomputable def OnWeakSpace {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    (f : E -> EReal) : WeakSpace Real E -> EReal :=
  fun x => f ((toWeakSpace Real E).symm x)

def WeakLowerSemicontinuityTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    IsExtendedRealConvex f ->
      (LowerSemicontinuous (OnWeakSpace f) <-> LowerSemicontinuous f)

end Stage1Instances.THM_M_1268

namespace Stage1Instances.THM_M_1268.ObligationTree

open Set

universe u

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
  forall r, IsClosed ((Stage1Instances.THM_M_1268.OnWeakSpace f) ⁻¹' Iic r)

def ConvexSublevelBridge : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    Stage1Instances.THM_M_1268.IsExtendedRealConvex f -> ConvexSublevels f

def WeakClosureTransportBridge : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    ConvexSublevels f -> NormClosedSublevels f -> WeakClosedSublevels f

def WeakToNormBridge : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    LowerSemicontinuous (Stage1Instances.THM_M_1268.OnWeakSpace f) ->
      LowerSemicontinuous f

theorem normClosedSublevels_iff {E : Type u} [TopologicalSpace E] (f : E -> EReal) :
    NormClosedSublevels f <-> LowerSemicontinuous f := by
  exact lowerSemicontinuous_iff_isClosed_preimage.symm

theorem weakClosedSublevels_iff {E : Type u}
    [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal) :
    WeakClosedSublevels f <->
      LowerSemicontinuous (Stage1Instances.THM_M_1268.OnWeakSpace f) := by
  exact lowerSemicontinuous_iff_isClosed_preimage.symm

/-- Checked child-to-parent composition for the substantive direction only. -/
theorem normToWeak_of_sublevel_bridges
    (hconvex : ConvexSublevelBridge.{u})
    (htransport : WeakClosureTransportBridge.{u}) :
    forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
      Stage1Instances.THM_M_1268.IsExtendedRealConvex f ->
        LowerSemicontinuous f ->
          LowerSemicontinuous (Stage1Instances.THM_M_1268.OnWeakSpace f) := by
  intro E _ _ f hf hlsc
  apply (weakClosedSublevels_iff f).mp
  exact htransport E f (hconvex E f hf) ((normClosedSublevels_iff f).mpr hlsc)

/-- Checked root assembly, conditional on all still-open mathematical bridges. -/
theorem root_of_bridges
    (hconvex : ConvexSublevelBridge.{u})
    (htransport : WeakClosureTransportBridge.{u})
    (hconverse : WeakToNormBridge.{u}) :
    Stage1Instances.THM_M_1268.WeakLowerSemicontinuityTarget.{u} := by
  intro E _ _ f hf
  constructor
  · exact hconverse E f
  · exact normToWeak_of_sublevel_bridges hconvex htransport E f hf

end Stage1Instances.THM_M_1268.ObligationTree

#check Convex.toWeakSpace_closure
#check Stage1Instances.THM_M_1268.ObligationTree.root_of_bridges
