import Mathlib.Analysis.LocallyConvex.WeakSpace
import Mathlib.Topology.Semicontinuity.Basic
import Mathlib.Data.EReal.Basic

/-!
# THM-M-1268: weak lower semicontinuity of convex functionals

This module freezes the statement boundary only. It does not prove the weak
lower-semicontinuity theorem.
-/

namespace Stage1Instances.THM_M_1268

universe u

/-- Convexity for a function with values in `(-infinity, +infinity]`.

`EReal` supplies both infinities, so the first conjunct excludes `-infinity`.
The displayed Jensen inequality is the extended-real convexity convention.
-/
def IsExtendedRealConvex {E : Type u} [AddCommGroup E] [Module Real E]
    (f : E -> EReal) : Prop :=
  (forall x, f x != (⊥ : EReal)) /\
    forall (x y : E) (a b : Real), 0 <= a -> 0 <= b -> a + b = 1 ->
      f (a • x + b • y) <= (a : EReal) * f x + (b : EReal) * f y

/-- The functional transported to the weak topology `sigma(E, E*)`. -/
noncomputable def OnWeakSpace {E : Type u} [NormedAddCommGroup E] [NormedSpace Real E]
    (f : E -> EReal) : WeakSpace Real E -> EReal :=
  fun x => f ((toWeakSpace Real E).symm x)

/-- The canonical topological weak-lower-semicontinuity target.

The equivalence retains both directions. Its substantive direction says that
norm lower semicontinuity plus convexity implies weak lower semicontinuity; the
reverse direction follows from the weak topology being coarser.
-/
def WeakLowerSemicontinuityTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    IsExtendedRealConvex f ->
      (LowerSemicontinuous (OnWeakSpace f) <-> LowerSemicontinuous f)

/-- Fully expanded alternate spelling of the canonical target. -/
def ExpandedTarget : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    ((forall x, f x != (⊥ : EReal)) /\
      forall (x y : E) (a b : Real), 0 <= a -> 0 <= b -> a + b = 1 ->
        f (a • x + b • y) <= (a : EReal) * f x + (b : EReal) * f y) ->
      (LowerSemicontinuous
          (fun x : WeakSpace Real E => f ((toWeakSpace Real E).symm x)) <->
        LowerSemicontinuous f)

/-- Checked transport to the fully expanded encoding. -/
theorem target_iff_expanded :
    WeakLowerSemicontinuityTarget.{u} <-> ExpandedTarget.{u} := by
  rfl

-- Structural mutations: these elaborate but are not alternate target claims.
def MutationRemovedConvexity : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    LowerSemicontinuous (OnWeakSpace f) <-> LowerSemicontinuous f

def MutationRealCodomain : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> Real),
    ConvexOn Real Set.univ f ->
      (LowerSemicontinuous
          (fun x : WeakSpace Real E => f ((toWeakSpace Real E).symm x)) <->
        LowerSemicontinuous f)

def MutationSequentialWeakLSC : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    IsExtendedRealConvex f ->
      ((forall (x : Nat -> WeakSpace Real E) (x0 : WeakSpace Real E),
          Filter.Tendsto x Filter.atTop (nhds x0) ->
            f ((toWeakSpace Real E).symm x0) <=
              Filter.liminf
                (fun n => f ((toWeakSpace Real E).symm (x n))) Filter.atTop) <->
        LowerSemicontinuous f)

def MutationReversedImplicationOnly : Prop :=
  forall (E : Type u) [NormedAddCommGroup E] [NormedSpace Real E] (f : E -> EReal),
    IsExtendedRealConvex f ->
      (LowerSemicontinuous (OnWeakSpace f) -> LowerSemicontinuous f)

end Stage1Instances.THM_M_1268

set_option pp.explicit true in
#print Stage1Instances.THM_M_1268.WeakLowerSemicontinuityTarget
