import Mathlib.Analysis.Normed.Operator.BanachSteinhaus

/-!
# THM-M-0312: exact Uniform Boundedness Principle statement

This module freezes the statement boundary and its checked alternate encoding. It does not assign
proof credit to the imported declarations.
-/

namespace Stage1Instances.THM_M_0312

universe uE uF uK uK2 uI

variable {E : Type uE} {F : Type uF} {K : Type uK} {K2 : Type uK2}
  [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
  [NontriviallyNormedField K] [NontriviallyNormedField K2]
  [NormedSpace K E] [NormedSpace K2 F]
  {sigma12 : K →+* K2} [RingHomIsometric sigma12]
  {I : Type uI} [CompleteSpace E]

/-- The exact normed-space Uniform Boundedness Principle selected at intake. -/
def UniformBoundednessTarget (g : I -> E →SL[sigma12] F) : Prop :=
  (forall x : E, exists C : Real, forall i : I, norm (g i x) <= C) ->
    exists C' : Real, forall i : I, norm (g i) <= C'

/-- The extended-nonnegative-supremum encoding published beside `banach_steinhaus`. -/
def UniformBoundednessISupTarget (g : I -> E →SL[sigma12] F) : Prop :=
  (forall x : E, (iSup fun i : I => (nnnorm (g i x) : ENNReal)) < ⊤) ->
    (iSup fun i : I => (nnnorm (g i) : ENNReal)) < ⊤

/-- The pinned real-bound declaration has exactly the frozen target type. -/
example {g : I -> E →SL[sigma12] F} : UniformBoundednessTarget g :=
  banach_steinhaus

/-- The two public mathlib formulations give a checked logical equivalence. Proof provenance and
eligibility remain responsibilities of the later anchor-audit phase. -/
theorem uniformBoundednessTarget_iff_iSupTarget {g : I -> E →SL[sigma12] F} :
    UniformBoundednessTarget g <-> UniformBoundednessISupTarget g := by
  constructor
  · intro _
    exact banach_steinhaus_iSup_nnnorm
  · intro _
    exact banach_steinhaus

-- Structural mutations. The validator requires each elaborated expression to differ from the root.
def mutationRemovedCompleteness
    {E : Type uE} {F : Type uF} {K : Type uK} {K2 : Type uK2}
    [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
    [NontriviallyNormedField K] [NontriviallyNormedField K2]
    [NormedSpace K E] [NormedSpace K2 F]
    {sigma12 : K →+* K2} [RingHomIsometric sigma12]
    {I : Type uI} (g : I -> E →SL[sigma12] F) : Prop :=
  (forall x : E, exists C : Real, forall i : I, norm (g i x) <= C) ->
    exists C' : Real, forall i : I, norm (g i) <= C'

def mutationChangedDomain {I : Type uI}
    (g : I -> Real →L[Real] Real) : Prop :=
  (forall x : Real, exists C : Real, forall i : I, norm (g i x) <= C) ->
    exists C' : Real, forall i : I, norm (g i) <= C'

def mutationChangedBinderScope (g : I -> E →SL[sigma12] F) : Prop :=
  (exists C : Real, forall x : E, forall i : I, norm (g i x) <= C) ->
    exists C' : Real, forall i : I, norm (g i) <= C'

def mutationNonemptyIndex [Nonempty I] (g : I -> E →SL[sigma12] F) : Prop :=
  UniformBoundednessTarget g

/-- The empty family is included, and its uniform bound is witnessed directly by zero. -/
theorem emptyIndexBoundary
    (g : Empty -> E →SL[sigma12] F) : UniformBoundednessTarget g := by
  intro _
  exact ⟨0, fun i => Empty.elim i⟩

end Stage1Instances.THM_M_0312

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0312.UniformBoundednessTarget
